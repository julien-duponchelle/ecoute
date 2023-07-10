import openai
from pydub import AudioSegment
from tempfile import NamedTemporaryFile


def transcribe(model, audio_file, response_format="json", audio_format="wav", **kwargs):
    """
    Transcribe the audio content to text.
    All arguments of openai.Audio.transcribe are supported

    :param file: The audio file object (not file name) to transcribe, in one of these formats: mp3, mp4, mpeg, mpga, m4a, wav, or webm.
    :param model: ID of the model to use.
    :param prompt: An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.
    :param response_format: The format of the transcript output, in one of these options: json, text, srt, verbose_json, or vtt. (default json)
    :param language: The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency.
    :param audio_format: The audio file format (mp3, wav, ...) default to wav, othert format require ffmpeg for other formats than wav
    """
    audio = AudioSegment.from_file(audio_file, format=audio_format)

    chunk_duration = 10 * 60

    result = None
    for slice in _slice(model, audio, audio_format, chunk_duration, **kwargs):
        if slice is None:
            break
        if result is None:
            result = slice
        else:
            result = _merge(result, slice)
    return _export(result, response_format)


def _export(transcript, response_format):
    if response_format is None or response_format == "json":
        return
    elif response_format == "text":
        return transcript.text
    else:
        raise NotImplementedError(
            f"{response_format} is not a supported format")


def _slice(model, audio, audio_format, chunk_duration, **kwargs):
    for slice in audio[::chunk_duration * 1000]:
        with NamedTemporaryFile(suffix="." + audio_format) as export:
            slice.export(export, format=audio_format)
            export.seek(0)
            yield openai.Audio.transcribe(model, export, **kwargs)


def _merge(o1, o2):
    o1.text += " " + o2.text
    return o1
