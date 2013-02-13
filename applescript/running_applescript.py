import os


def main():
    cmd = """osascript <<END
    set vol to output volume of (get volume settings)
    set vol_interval to 5
    if vol > (100 - vol_interval) then
	set volume output volume 100
    else
	set volume output volume (vol + 5)
    end if
    END"""
    os.system(cmd)


if __name__ == '__main__':
    main()
