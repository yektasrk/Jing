import subprocess
import time
import mido


class Audio:
    def __init__(self):
        self.fluid = subprocess.Popen(["fluidsynth", "--audio-driver=alsa",
                                       "/usr/share/sounds/sf2/FluidR3_GM.sf2"],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out = subprocess.run(["aconnect", "-o"],
                             capture_output=True, text=True).stdout
        while("FLUID Synth" not in out):
            print("wait")
            time.sleep(1)
            out = subprocess.run(["aconnect", "-o"],
                                 capture_output=True, text=True).stdout

        fluid_port = ""
        ports = mido.get_output_names()
        for port in ports:
            if "FLUID Synth" in port:
                fluid_port = port
        self.port = mido.open_output(fluid_port)

    def start_note(self, midi):
        channel, note, loudness, program = midi
        msg = mido.Message('program_change', program = program, channel = channel)
        self.port.send(msg)
        msg = mido.Message('note_on', note=note, velocity=loudness)
        self.port.send(msg)

    def stop_note(self, channel):
        pass

    def end(self):
        self.fluid.terminate()
