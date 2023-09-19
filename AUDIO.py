import struct
try:
    import audioop
except ImportError:
    import pyaudioop as audioop
from io import BytesIO


def extract_wav_headers(data):
    pos = 12  # The size of the RIFF chunk descriptor
    subchunks = []
    while pos + 8 <= len(data) and len(subchunks) < 10:
        subchunk_id = data[pos:pos + 4]
        subchunk_size = struct.unpack_from('<I', data[pos + 4:pos + 8])[0]
        subchunks.append([subchunk_id, pos, subchunk_size])
        if subchunk_id == b'data':
            break
        pos += subchunk_size + 8

    return subchunks

def read_wav_audio(data, headers=None):
    if not headers:
        headers = extract_wav_headers(data)
    
    print("Data:", str(data)[:100],"headers: "+str(headers))
    fmt = [x for x in headers if x[0] == b'fmt '][0]
    
    pos = fmt[1] + 8
    audio_format = struct.unpack_from('<H', data[pos:pos + 2])[0]
    channels = struct.unpack_from('<H', data[pos + 2:pos + 4])[0]
    sample_rate = struct.unpack_from('<I', data[pos + 4:pos + 8])[0]
    bits_per_sample = struct.unpack_from('<H', data[pos + 14:pos + 16])[0]
    data_hdr = headers[-1]
    pos = data_hdr[1] + 8
    return (audio_format, channels, sample_rate, bits_per_sample, data[pos:pos + data_hdr[2]])

def spawnsound(file, frame_rate2): 
    try:
        file = file if isinstance(file, (str, bytes)) else file.read()
    except(OSError):
        d = b''
        reader = file.read(2 ** 31 - 1)
        while reader:
            d += reader
            reader = file.read(2 ** 31 - 1)
        data = d

    wav_data = read_wav_audio(file)

    channels = wav_data[1]
    sample_width = wav_data[3] // 8
    frame_rate = wav_data[2]
    data = wav_data[4]
    if sample_width == 1:
        data = audioop.bias(data, 1, -128)
    if sample_width == 3:
        byte_buffer = BytesIO()
        pack_fmt = 'BBB' if isinstance(data[0], int) else 'ccc'
        i = iter(data)
        padding = {False: b'\x00', True: b'\xFF'}
        for b0, b1, b2 in zip(i, i, i):
            byte_buffer.write(padding[b2 > b'\x7f'[0]])
            old_bytes = struct.pack(pack_fmt, b0, b1, b2)
            byte_buffer.write(old_bytes)

        data = byte_buffer.getvalue()
        sample_width = 4
    return audioop.ratecv(data, int(sample_width),
                                    int(channels), int(frame_rate),
                                    int(frame_rate*frame_rate2), None)