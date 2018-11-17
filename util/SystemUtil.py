import alsaaudio


class AudioUtility:

    def __init__(self):
        self.m = alsaaudio.Mixer()

    def increaseVolume(self):
        vol = self.m.getvolume()
        if vol[0] >= 100:
            vol[0] = 100
        newVol = min(100, int(vol[0]) + 15)
        print('Volume changed to: ', newVol)
        self.m.setvolume(newVol)

    def decreaseVolume(self):
        vol = self.m.getvolume()
        if vol[0] >= 100:
            vol[0] = 100
        newVol = max(0, int(vol[0] - 15))
        print('Volume changed to: ', newVol)
        self.m.setvolume(newVol)


def main():
    util = AudioUtility()
    util.increaseVolume()
    util.increaseVolume()


if __name__ == '__main__':
    main()
