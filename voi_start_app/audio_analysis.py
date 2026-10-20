from pathlib import Path
import tempfile

import librosa
import numpy as np
from pydub import AudioSegment


def convert_to_wav(input_path: str) -> str:
    """Convert browser audio such as WebM into a temporary WAV file."""
    temporary_wav = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False,
    )
    temporary_wav.close()

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(22050)
    audio.export(temporary_wav.name, format="wav")

    return temporary_wav.name


def frequency_to_note(frequency: float) -> str | None:
    if not frequency or not np.isfinite(frequency) or frequency <= 0:
        return None

    return str(librosa.hz_to_note(frequency))


def analyze_audio(file_path: str) -> dict:
    wav_path = convert_to_wav(file_path)

    try:
        audio, sample_rate = librosa.load(
            wav_path,
            sr=22050,
            mono=True,
        )

        if len(audio) == 0:
            raise ValueError("The audio file is empty.")

        return extract_features(audio, sample_rate)
    finally:
        Path(wav_path).unlink(missing_ok=True)


def extract_features(audio: np.ndarray, sample_rate: int) -> dict:
    # Remove very quiet background sections.
    intervals = librosa.effects.split(
        audio,
        top_db=30,
    )
    voiced_audio = (
        np.concatenate([audio[start:end] for start, end in intervals])
        if len(intervals)
        else audio
    )

    if len(voiced_audio) < sample_rate:
        raise ValueError("At least one second of usable audio is required.")

    # Fundamental frequency estimation.
    f0, voiced_flag, voiced_probability = librosa.pyin(
        voiced_audio,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C6"),
        sr=sample_rate,
        frame_length=2048,
        hop_length=256,
    )

    valid_f0 = f0[
        np.isfinite(f0)
        & (voiced_flag == True)
        & (voiced_probability >= 0.6)
    ]

    if len(valid_f0) == 0:
        raise ValueError("Could not detect a stable singing pitch.")

    # Percentiles reduce the effect of accidental octave errors.
    low_frequency = float(np.percentile(valid_f0, 5))
    high_frequency = float(np.percentile(valid_f0, 95))
    median_frequency = float(np.median(valid_f0))

    # Loudness.
    rms = librosa.feature.rms(
        y=voiced_audio,
        frame_length=2048,
        hop_length=256,
    )[0]

    # Spectral features.
    centroid = librosa.feature.spectral_centroid(
        y=voiced_audio,
        sr=sample_rate,
        hop_length=256,
    )[0]

    bandwidth = librosa.feature.spectral_bandwidth(
        y=voiced_audio,
        sr=sample_rate,
        hop_length=256,
    )[0]

    rolloff = librosa.feature.spectral_rolloff(
        y=voiced_audio,
        sr=sample_rate,
        roll_percent=0.85,
        hop_length=256,
    )[0]

    zero_crossing_rate = librosa.feature.zero_crossing_rate(
        voiced_audio,
        hop_length=256,
    )[0]

    # MFCCs are useful as a general timbre representation.
    mfcc = librosa.feature.mfcc(
        y=voiced_audio,
        sr=sample_rate,
        n_mfcc=13,
        hop_length=256,
    )

    # Pitch stability: lower standard deviation generally means steadier pitch.
    pitch_stability = float(
        1 / (1 + np.std(librosa.hz_to_midi(valid_f0)))
    )

    return {
        "sample_rate": sample_rate,
        "duration_seconds": round(len(audio) / sample_rate, 2),

        "pitch": {
            "low_hz": round(low_frequency, 2),
            "high_hz": round(high_frequency, 2),
            "median_hz": round(median_frequency, 2),
            "low_note": frequency_to_note(low_frequency),
            "high_note": frequency_to_note(high_frequency),
            "median_note": frequency_to_note(median_frequency),
            "detected_frames": int(len(valid_f0)),
            "stability_score": round(pitch_stability, 3),
        },

        "loudness": {
            "average_rms": round(float(np.mean(rms)), 5),
            "maximum_rms": round(float(np.max(rms)), 5),
            "dynamic_range": round(
                float(np.percentile(rms, 95) - np.percentile(rms, 5)),
                5,
            ),
        },

        "tone": {
            "spectral_centroid_hz": round(float(np.mean(centroid)), 2),
            "spectral_bandwidth_hz": round(float(np.mean(bandwidth)), 2),
            "spectral_rolloff_hz": round(float(np.mean(rolloff)), 2),
            "zero_crossing_rate": round(float(np.mean(zero_crossing_rate)), 5),
            "mfcc_means": [
                round(float(value), 3)
                for value in np.mean(mfcc, axis=1)
            ],
        },
    }