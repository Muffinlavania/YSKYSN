import struct,os
try:
    import audioop
except ImportError:
    import pyaudioop as audioop
from io import BytesIO

'''
 File "/Users/muffinlavania/Downloads/YSKYSN-main/yskysnsolo.py", line 475, in startmusic
    sound(changespeed(SOUND("YSKYSN/dial1.wav" if level==1 else "YSKYSN/dial2.wav"), SPEEDS[str(speed)]*s_offset).raw_data,False,'DIAL')
  File "/Users/muffinlavania/Downloads/YSKYSN-main/yskysnsolo.py", line 13, in SOUND
    return from_safe_wav(AUDIO.AudioSegment,open(file_name(path), mode='rb'))
  File "/Users/muffinlavania/Downloads/YSKYSN-main/yskysnsolo.py", line 8, in from_safe_wav
    obj = cls(data=file)
  File "/Users/muffinlavania/Downloads/YSKYSN-main/AUDIO.py", line 63, in __init__
    self.frame_width = self[1] * self[2]
TypeError: 'AudioSegment' object is not subscriptable

'''


def extract_wav_headers(data):
    pos = 12  # The size of the RIFF chunk descriptor
    subchunks = []
    while pos + 8 <= len(data) and len(subchunks) < 10:
        subchunk_id = data[pos:pos + 4]
        subchunk_size = struct.unpack_from('<I', data[pos + 4:pos + 8])[0]
        subchunks.append((subchunk_id, pos, subchunk_size))
        if subchunk_id == b'data':
            break
        pos += subchunk_size + 8

    return subchunks

def which(program):
    # Add .exe program extension for windows support
    if os.name == "nt" and not program.endswith(".exe"):
        program += ".exe"
    envdir_list = [os.curdir] + os.environ["PATH"].split(os.pathsep)
    for envdir in envdir_list:
        program_path = os.path.join(envdir, program)
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return program_path

def read_wav_audio(data, headers=None):
    if not headers:
        headers = extract_wav_headers(data)
    fmt = [x for x in headers if x[0] == b'fmt '][0]
    pos = fmt[1] + 8
    audio_format = struct.unpack_from('<H', data[pos:pos + 2])[0]
    channels = struct.unpack_from('<H', data[pos + 2:pos + 4])[0]
    sample_rate = struct.unpack_from('<I', data[pos + 4:pos + 8])[0]
    bits_per_sample = struct.unpack_from('<H', data[pos + 14:pos + 16])[0]
    data_hdr = headers[-1]
    pos = data_hdr[1] + 8
    return (audio_format, channels, sample_rate, bits_per_sample, data[pos:pos + data_hdr[2]])


class AudioSegment(object):
  converter = "avconv" if which("avconv") else "ffmpeg"  # either ffmpeg or avconv
  def __init__(self, data=None, *args, **kwargs):
      try:
          data = data if isinstance(data, (str, bytes)) else data.read()
      except(OSError):
          d = b''
          reader = data.read(2 ** 31 - 1)
          while reader:
              d += reader
              reader = data.read(2 ** 31 - 1)
          data = d

      wav_data = read_wav_audio(data)

      self.channels = wav_data[1]
      self.sample_width = wav_data[3] // 8
      self.frame_rate = wav_data[2]
      self.frame_width = self[1] * self[2]
      self._data = wav_data[4]
      if self.sample_width == 1:
          self._data = audioop.bias(self._data, 1, -128)
      if self.sample_width == 3:
          byte_buffer = BytesIO()
          pack_fmt = 'BBB' if isinstance(self._data[0], int) else 'ccc'
          i = iter(self._data)
          padding = {False: b'\x00', True: b'\xFF'}
          for b0, b1, b2 in zip(i, i, i):
              byte_buffer.write(padding[b2 > b'\x7f'[0]])
              old_bytes = struct.pack(pack_fmt, b0, b1, b2)
              byte_buffer.write(old_bytes)

          self._data = byte_buffer.getvalue()
          self.sample_width = 4
          self.frame_width = self.channels * self.sample_width

      super(AudioSegment, self).__init__(*args, **kwargs)

  @property
  def raw_data(self):
    return self._data

  def _spawn(self, data, overrides={}):
      if isinstance(data, list):
          data = b''.join(data)
      if hasattr(data, 'read'):
          if hasattr(data, 'seek'):
              data.seek(0)
          data = data.read()

      metadata = {
          'sample_width': self.sample_width,
          'frame_rate': self.frame_rate,
          'frame_width': self.frame_width,
          'channels': self.channels
      }
      metadata.update(overrides)
      return self.__class__(data=data, metadata=metadata)

  #def set_frame_rate(self, frame_rate):
  #    if frame_rate == self.frame_rate:
  #        return self
  #    if self._data:
  #        converted, _ = audioop.ratecv(self._data, self.sample_width,
  #                                      self.channels, self.frame_rate,
  #                                      frame_rate, None)
  #    else:
  #        converted = self._data
  #
  #    return self._spawn(data=converted,
  #                        overrides={'frame_rate': frame_rate})
