import numpy as np
from scipy.io.wavfile import write
from typing import Optional


def get_int_input(
    input_name: str,
    min_value: int,
    max_value: int,
    default_value: Optional[int] = None,
    is_optional: bool = False,
) -> int:
    """
    Gets, validates, and returns integer input from the user.

    Parameters:
    - input_name (str): Name of the input parameter for user reference.
    - default_value (Optional[int]): Default value if input is optional.
    - min_value (int): Minimum acceptable value.
    - max_value (int): Maximum acceptable value.
    - is_optional (bool): If True, allows the input to be optional.

    Returns:
    - int: Validated integer input from the user.
    """
    output = None
    prompt = f"\nPlease provide the desired {input_name} (between {min_value} and {max_value}): "
    if is_optional:
        prompt = "[Optional]" + f"\nDefault value is {default_value}" + prompt

    while True:
        user_input = input(prompt).strip()
        if is_optional and user_input == "":
            print(f"\nUsing the default value {default_value}\n")
            return default_value
        try:
            output = int(user_input)
            if min_value <= output <= max_value:
                print(f"\nThe provided value of {output} will be used.\n")
                return output
            else:
                print(
                    f"The provided value should be within (inclusive) range of {min_value} and {max_value}"
                )
        except ValueError:
            print("Please enter a valid integer.")


def generate_audio_data(
    sample_rate: int, frequency_base: int, frequency_diff: int, duration: int
) -> np.ndarray:
    """
    Generates binaural beat audio data as a stereo signal.

    Parameters:
    - sample_rate (int): The sample rate in Hz.
    - frequency_base (int): The base frequency for the left channel.
    - frequency_diff (int): Frequency difference for the right channel.
    - duration (int): Duration of the audio in seconds.

    Returns:
    - np.ndarray: A stereo waveform array normalized to 16-bit PCM format.
    """
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate left and right audio signals
    left_wave = np.sin(2 * np.pi * frequency_base * t)
    right_wave = np.sin(2 * np.pi * (frequency_base + frequency_diff) * t)
    # Combine into a stereo signal
    stereo_wave = np.vstack((left_wave, right_wave)).T
    # Normalize to 16-bit PCM range (-32767 to 32767)
    stereo_wave = np.int16(stereo_wave / np.max(np.abs(stereo_wave)) * 32767)
    return stereo_wave


if __name__ == "__main__":
    sample_rate = 44100  # Samples per second
    frequency_base = get_int_input(
        input_name="Frequency Base",
        min_value=100,
        max_value=2000,
        default_value=1000,
        is_optional=True,
    )
    # Difference between left and right frequencies (binaural beat frequency)
    frequency_diff = get_int_input(input_name="Frequency", min_value=1, max_value=60)
    # Duration in seconds
    duration = get_int_input(
        input_name="Duration in seconds", min_value=10, max_value=3600
    )
    stereo_wave = generate_audio_data(
        sample_rate, frequency_base, frequency_diff, duration
    )
    # Save as a .wav file
    write(f"binaural_beat_{frequency_diff}Hz.wav", sample_rate, stereo_wave)

    print(
        f"\n\nBinaural beat audio file 'binaural_beat_{frequency_diff}Hz.wav' generated!\n\n"
    )
