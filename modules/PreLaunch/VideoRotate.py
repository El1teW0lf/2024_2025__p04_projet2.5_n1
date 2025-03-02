import subprocess
def rotate_video(input_path, output_path):
      
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "transpose=2",
        "-codec", "libx264",
        output_path
    ]

    subprocess.run(command, check=True)

name = "screamer_surveillant"
rotate_video(f"/Users/victor/Documents/NSI/Project2,5/screamers/raws/{name}/{name}.mp4", f"/Users/victor/Documents/NSI/Project2,5/screamers/plane/{name}/{name}.mp4")
