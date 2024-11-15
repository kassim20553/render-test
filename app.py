import os
from flask import Flask, request, jsonify
from gtts import
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

app = Flask(__name__)

# Directory to save videos
VIDEO_DIR = "videos"

# Ensure the videos directory exists
os.makedirs(VIDEO_DIR, exist_ok=True)

# Step 1: Convert text to speech
def text_to_speech(text, audio_file="narration.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(audio_file)
    return audio_file

# Step 2: Generate placeholder image slides for the text
def generate_images(text, num_images=5):
    images = []
    for i in range(num_images):
        img = Image.new('RGB', (1280, 720), color=(73, 109, 137))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((50, 360), text, font=font, fill="white")
        img_path = f"slide_{i}.png"
        img.save(img_path)
        images.append(img_path)
    return images

# Step 3: Create a video from images and narration
def create_video_with_audio(image_files, audio_file, output_file, duration=5):
    clips = [ImageClip(img).set_duration(duration) for img in image_files]
    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_file)
    video = video.set_audio(audio)
    video.write_videofile(output_file, fps=24)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.get_json()
    text = data.get("text", "This is an example of a text-to-video generation script using Python.")
    duration_per_slide = data.get("duration_per_slide", 5)
    num_images = data.get("num_images", 5)
    output_video_path = os.path.join(VIDEO_DIR, "text_to_video_output.mp4")

    # Run the steps
    try:
        audio_file = text_to_speech(text)
        image_files = generate_images(text, num_images)
        create_video_with_audio(image_files, audio_file, output_video_path, duration_per_slide)
        return jsonify({"message": "Video generated successfully!", "video_path": output_video_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
