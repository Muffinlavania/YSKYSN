import random,time,sys,pygame
pygame.mixer.init(frequency=24000)
pygame.mixer.music.load("YSKYSN/dial1.mp3")
pygame.mixer.music.play(-1)
time.sleep(10)
pygame.mixer.quit()
def rand():
  for i in range(1000):
    if random.randint(0,100)==100:
      print("DUDE WHY")
    if random.randrange(0,100)==100:
      print("B) will never print since its actually useful")

def clearline(amo=1):
  sys.stdout.write(f'\x1b[1A\x1b[2K'*amo)
def cltest():
  print("hi\n"*5)
  clearline(4)
  print("ok")






import struct,os
#from collections import namedtuple

#WavSubChunk = namedtuple('WavSubChunk', ['id', 'position', 'size'])
def extract_wav_headers(data):
    # def search_subchunk(data, subchunk_id):
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


def read_wav_audio(data, headers=None):
    if not headers:
        headers = extract_wav_headers(data)
    fmt = fmt[0]
    pos = fmt.position + 8
    audio_format = struct.unpack_from('<H', data[pos:pos + 2])[0]
    channels = struct.unpack_from('<H', data[pos + 2:pos + 4])[0]
    sample_rate = struct.unpack_from('<I', data[pos + 4:pos + 8])[0]
    bits_per_sample = struct.unpack_from('<H', data[pos + 14:pos + 16])[0]
    data_hdr = headers[-1]
    pos = data_hdr.position + 8
    return (audio_format, channels, sample_rate, bits_per_sample, data[pos:pos + data_hdr.size])

def _fd_or_path_or_tempfile(fd, mode='w+b', tempfile=True):
  return open(fd, mode=mode), True  


def which(program):
    """
    Mimics behavior of UNIX which command.
    """
    # Add .exe program extension for windows support
    if os.name == "nt" and not program.endswith(".exe"):
        program += ".exe"

    envdir_list = [os.curdir] + os.environ["PATH"].split(os.pathsep)

    for envdir in envdir_list:
        program_path = os.path.join(envdir, program)
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return program_path
          

class AudioSegment(object):
  converter = "avconv" if which("avconv") else "ffmpeg"  # either ffmpeg or avconv
  @classproperty
  def ffmpeg(cls):
      return cls.converter

  @ffmpeg.setter
  def ffmpeg(cls, val):
      cls.converter = val

  DEFAULT_CODECS = {
      "ogg": "libvorbis"
  }
  def __init__(self, data=None, *args, **kwargs):
      
      # normal construction
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

      self.channels = wav_data.channels
      self.sample_width = wav_data.bits_per_sample // 8
      self.frame_rate = wav_data.sample_rate
      self.frame_width = self.channels * self.sample_width
      self._data = wav_data.raw_data
      if self.sample_width == 1:
          # convert from unsigned integers in wav
          self._data = audioop.bias(self._data, 1, -128)

      # Convert 24-bit audio to 32-bit audio.
      # (stdlib audioop and array modules do not support 24-bit data)
      if self.sample_width == 3:
          byte_buffer = BytesIO()

          # Workaround for python 2 vs python 3. _data in 2.x are length-1 strings,
          # And in 3.x are ints.
          pack_fmt = 'BBB' if isinstance(self._data[0], int) else 'ccc'

          # This conversion maintains the 24 bit values.  The values are
          # not scaled up to the 32 bit range.  Other conversions could be
          # implemented.
          i = iter(self._data)
          padding = {False: b'\x00', True: b'\xFF'}
          for b0, b1, b2 in izip(i, i, i):
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
      # accept lists of data chunks
      if isinstance(data, list):
          data = b''.join(data)
      #if isinstance(data, array.array):
      #    try:
      #        data = data.tobytes()
      #    except:
      #        data = data.tostring()
      # accept file-like objects
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

  def fsdecode(filename):
    PathLikeTypes = (str, bytes)
    if sys.version_info >= (3, 6):
        PathLikeTypes += (os.PathLike,)
    if isinstance(filename, PathLikeTypes):
        return os.fsdecode(filename)

    raise TypeError("type {0} not accepted by fsdecode".format(type(filename)))
  def _from_safe_wav(cls, file):
    file, close_file = _fd_or_path_or_tempfile(file, 'rb', tempfile=False)
    file.seek(0)
    obj = cls(data=file)
    if close_file:
        file.close()
    return obj

  def from_file(cls, file, format=None, codec=None, parameters=None, start_second=None, duration=None, **kwargs):
      orig_file = file
      try:
          filename = fsdecode(file)
      except TypeError:
          filename = None
      file, close_file = _fd_or_path_or_tempfile(file, 'rb', tempfile=False)

      if format:
          format = format.lower()
          format = AUDIO_FILE_EXT_ALIASES.get(format, format)

      def is_format(f):
          f = f.lower()
          if format == f:
              return True

          if filename:
              return filename.lower().endswith(".{0}".format(f))

          return False

      if is_format("wav"):
          try:
              if start_second is None and duration is None:
                  return cls._from_safe_wav(file)
              elif start_second is not None and duration is None:
                  return cls._from_safe_wav(file)[start_second*1000:]
              elif start_second is None and duration is not None:
                  return cls._from_safe_wav(file)[:duration*1000]
              else:
                  return cls._from_safe_wav(file)[start_second*1000:(start_second+duration)*1000]
          except:
              file.seek(0)

  def set_frame_rate(self, frame_rate):
      if frame_rate == self.frame_rate:
          return self
      if self._data:
          converted, _ = audioop.ratecv(self._data, self.sample_width,
                                        self.channels, self.frame_rate,
                                        frame_rate, None)
      else:
          converted = self._data

      return self._spawn(data=converted,
                          overrides={'frame_rate': frame_rate})
