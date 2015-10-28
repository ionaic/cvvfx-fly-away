ffmpeg -r 10 -pattern_type glob -i "frames/*.JPG" -vf scale=-1:1080 out.mp4
ffmpeg -r 10 -pattern_type glob -i "input_frames/*.JPG" -vf scale=-1:1080 out_unedited.mp4
