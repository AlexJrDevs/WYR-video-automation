#Moviepy + Other Libraries
from moviepy.editor import *
from moviepy.video.VideoClip import *
from moviepy.video.fx import *
from PIL import Image
from moviepy.config import change_settings
image_magick_path = r"C:\Program Files\ImageMagick-7.1.1-Q16\convert.exe"
change_settings({"IMAGEMAGICK_BINARY": image_magick_path})

#Other Scripts
from questions import QuestionManager, data_file
from tiktokvoice import tts

#Base Imports
import os
import random
import datetime
import tempfile


##################################################################################################################################################
# Variables

#Background
background_video_path = "Background\Template.mp4"
background_video = VideoFileClip(background_video_path)
video_width = 1080
fps = 24

follow_clip = "Background\watch_video.mp4"


# BG Audios
BG_volume = 0.2 # 1 is full volume

background_audio_path = "Background\BackgroundAudio.mp3"
background_audio_clip = AudioFileClip(background_audio_path)
background_audio_clip = background_audio_clip.volumex(BG_volume)

# SFX
sfx_volume = 0.7

percentage_audio_path = "Background\ding.mp3"
percentage_sound = AudioFileClip("Background\ding.mp3")
percentage_sound = percentage_sound.volumex(sfx_volume)

woosh_audio_path = "Background\woosh.mp3"
woosh_audio_clip = AudioFileClip(woosh_audio_path)
woosh_audio_clip = woosh_audio_clip.volumex(sfx_volume)

#Text
font_size = 60
stroke_width = 20
stroke_color = 'black'
text_color = 'white'
font = 'Arial-Bold'

# Load images and resize them to fit within the desired dimensions
image_size = ( 960, 540 )
movement_duration = 0.1 # Adjust this value to change how fast it gets to destination
target_x = 50

start1_x = -2000
start2_x = 1000


#Percentages
Pfont_size = 90
Pstroke_width = 15
Pstroke_color = 'black'
Pfont = 'Arial-Bold'

#Find length of list and how many videos required to create videos
length = len(QuestionManager(data_file).question_data)
list_num = length // 2
total_duration = 0
n = 1


# Create an empty list to store video filenames
generated_video_filenames = []
question_manager = QuestionManager(data_file)
folder_name = "videos" # Folder name to save videos
first_voice = True
video_count = 0


##################################################################################################################################################




while list_num > 0:

    video_count += 1

    question1_text, question1_image_path = question_manager.get_section_question_with_image(1)
    question2_text, question2_image_path = question_manager.get_section_question_with_image(2)

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')


    ##################################################################################################################################################
    #TTS Generation
    if(first_voice == True):
        VOICE = 'en_male_ukneighbor'
    else:
        VOICE = 'en_us_009'

    question1_audio_path = f"question1_audio_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    question2_audio_path = f"question2_audio_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"

    # Generate TikTok TTS audio clips
    print("Generating audio for question 1:", question1_text)
    question1_audio_data = tts(f"Would you rather {question1_text}", VOICE, question1_audio_path)

    print("Generating audio for question 2:", question2_text)
    question2_audio_data = tts(f"Or {question2_text}",  VOICE, question2_audio_path)

    if not question1_audio_data or not question2_audio_data:
        print("TikTok TTS audio generation failed")
        continue
    
    # Load audio clips using MoviePy
    question1_audio_clip = AudioFileClip(question1_audio_data)
    question2_audio_clip = AudioFileClip(question2_audio_data)


    ##################################################################################################################################################





    ##################################################################################################################################################
    #Clips Durations

     # Set the duration of text clips to match the total audio duration
    total_audio_duration = question1_audio_clip.duration + question2_audio_clip.duration + percentage_sound.duration

    video_length = total_audio_duration + percentage_sound.duration # Calculate the extended video length 

    question2_duration = video_length - question1_audio_clip.duration

    total_duration += video_length
    
    ##################################################################################################################################################




    ##################################################################################################################################################
    #Images + Image Movement Creation
    question1_image = Image.open(question1_image_path)
    question1_image = question1_image.resize((image_size), Image.LANCZOS)

    question2_image = Image.open(question2_image_path)
    question2_image = question2_image.resize((image_size), Image.LANCZOS)

    # Save temporary image files
    temp_question1_image_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
    temp_question2_image_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name

    question1_image.save(temp_question1_image_path)
    question2_image.save(temp_question2_image_path)

    # Create ImageSequenceClip objects
    question1_image_clip = ImageSequenceClip([temp_question1_image_path], fps = fps).set_duration(video_length)
    question2_image_clip = ImageSequenceClip([temp_question2_image_path], fps = fps).set_duration(question2_duration)

    # For image1_clip movement
    image1_clip = question1_image_clip.set_position(lambda t: (
        int(min(max(start1_x + (target_x - start1_x) * t / movement_duration, start1_x), target_x)), 100))

    # For image2_clip movement
    image2_clip = question2_image_clip.set_position(lambda t: (
        int(min(max(start2_x + (target_x - start2_x) * t  / movement_duration, target_x), start2_x)), 1235)).set_start(question1_audio_clip.duration)

    ##################################################################################################################################################





    ###################################################################################################################################################
    #Clips Text Stroke + Normal Text

    # Create text clips for the questions
    question1_text_clip_stroke = TextClip(
        question1_text,
        font= font,
        fontsize=font_size,
        color=text_color,
        stroke_width=stroke_width,
        stroke_color= stroke_color,
        size=(video_width*3/4 + stroke_width, None),
        method='caption',
        align="north",
    ).set_duration(video_length).set_start(0).set_position(('center', 600))


    question2_text_clip_stroke = TextClip(
        question2_text,
        font= font,
        fontsize=font_size,
        color=text_color,
        stroke_width=stroke_width,
        stroke_color= stroke_color,
        size=(video_width*3/4 + stroke_width, None),
        method='caption',
        align="north",
    ).set_duration(question2_duration).set_start(question1_audio_clip.duration).set_position(('center', 1200))

    question1_text_clip = TextClip(
        question1_text,
        font= font,
        fontsize=font_size,
        color=text_color,
        size=(video_width*3/4, None),
        method='caption',
        align="north",
    ).set_duration(video_length).set_start(0).set_position(('center', 600))



    question2_text_clip = TextClip(
        question2_text,
        font= font,
        fontsize=font_size,
        color=text_color,
        size=(video_width*3/4, None),
        method='caption',
        align="north",
    ).set_duration(question2_duration).set_start(question1_audio_clip.duration).set_position(('center', 1200))


    # What Video the person is on:

    video_info = TextClip(
        f"{video_count}/",
        font= font,
        fontsize=font_size,
        color='black',
        size=(video_width*3/4, None),
        method='caption',
        align="north",
    ).set_duration(video_length).set_start(0).set_position((120, 1100))

   ##################################################################################################################################################





   ###################################################################################################################################################
   #Percentage Generator

    def generate_random_percentages():
        percentage1 = random.randint(30, 86)
        while(percentage1 == 50):
            percentage1 = random.randint(30, 86)
        percentage2 = 100 - percentage1
        return percentage1, percentage2

    # Generate two random percentages that add up to 100
    percentage1, percentage2 = generate_random_percentages()

    light_green = '#90ee90'
    light_red = '#D21404'

    percentage1_color = light_green if percentage1 >= 51 else light_red
    percentage2_color = light_green if percentage2 >= 51 else light_red

    # Create text clips for the random percentages
    percentage1_text = f"{percentage1}%"
    percentage2_text = f"{percentage2}%"

    # Percentage starter and ender
    percentage_start = video_length - 1

    # Create text clips for the stroke effect (with stroke)
    percentage1_text_clip_stroke = TextClip(
        percentage1_text,
        font=Pfont,
        fontsize=Pfont_size,
        color=percentage1_color,
        stroke_width=Pstroke_width,
        stroke_color=Pstroke_color,
        method='caption',
        align="north"
    ).set_duration(video_length - percentage_start).set_start(percentage_start).set_position(('center', 280))

    percentage2_text_clip_stroke = TextClip(
        percentage2_text,
        font=Pfont,
        fontsize=Pfont_size,
        color=percentage2_color,
        stroke_width=Pstroke_width,
        stroke_color=Pstroke_color,
        method='caption',
        align="north"
    ).set_duration(video_length - percentage_start).set_start(percentage_start).set_position(('center', 1500))


    # Create regular text clips for the random percentages
    percentage1_text_clip = TextClip(
        percentage1_text,
        font=Pfont,
        fontsize=Pfont_size,
        color=percentage1_color,
        method='caption',
        align="north"
    ).set_duration(video_length - percentage_start).set_start(percentage_start).set_position(('center', 280))

    percentage2_text_clip = TextClip(
        percentage2_text,
        font=Pfont,
        fontsize=Pfont_size,
        color=percentage2_color,
        method='caption',
        align="north"
    ).set_duration(video_length - percentage_start).set_start(percentage_start).set_position(('center', 1500))

    ####################################################################################################################################################




    ####################################################################################################################################################
    #Composition Section

    # Composite the video with the questions and stroke effects
    composition = CompositeVideoClip([
        background_video.set_duration(video_length),

        #Image Load
        image1_clip,
        image2_clip,

        #Stroke Load  
        question1_text_clip_stroke,
        question2_text_clip_stroke,

        #Text Load
        question1_text_clip,
        question2_text_clip,

        #Percentages
        percentage1_text_clip_stroke,
        percentage2_text_clip_stroke,
        percentage1_text_clip,  
        percentage2_text_clip,  

        video_info,

    ])


    # Add audio clips to the composition
    combined_audio = CompositeAudioClip([
        woosh_audio_clip.set_start(0),
        woosh_audio_clip.set_start(question1_audio_clip.duration),

        question1_audio_clip.set_start(0),
        question2_audio_clip.set_start(question1_audio_clip.duration),
        
        percentage_sound.set_start(percentage_start).volumex(0.7),
        background_audio_clip.set_duration(total_audio_duration),  # Include background audio
    ])


    composition = composition.set_audio(combined_audio)

    # Generate unique file names for each video
    output_file_name = f"tiktok_video_{timestamp}.mp4"

    # Export the final video
    composition.write_videofile(output_file_name, codec='libx264', audio_codec='aac', fps=24)


    # Append the generated video filename to the list
    generated_video_filenames.append(output_file_name)

    # Now, create a new composition combining the follow_clip and video_info
    if first_voice:
        follow_video = VideoFileClip(follow_clip)
        follow_with_info = CompositeVideoClip([
            follow_video,
            video_info.set_duration(follow_video.duration).set_position((120, 1100)),
        ])
        follow_with_info.write_videofile("follow_video.mp4", codec='libx264', audio_codec='aac', fps=24)
        generated_video_filenames.append("follow_video.mp4")
    
    first_voice = False

    ###################################################################################################################################################




    ###################################################################################################################################################
    
    

    # Delete the audio files
    os.remove(question1_audio_path)
    os.remove(question2_audio_path)

    # Remove Questions and file
    question_manager.remove_used_question(1)
    question_manager.remove_used_question(2)

    print("Total duration for the question: ", total_duration)

    if total_duration >= 10:
        combines_videos()
        first_voice = True
        total_duration = 0  # Reset total duration counter
        video_count = 0

    

    def combines_videos():
        # Load the generated video clips
        generated_clips = [VideoFileClip(filename) for filename in generated_video_filenames]

         # Calculate the total number of generated clips
        total_generated_clips = len(generated_clips)

        # Concatenate the generated clips
        concatenated_clip = concatenate_videoclips(generated_clips)



        total_clips_text = TextClip(
            f"{total_generated_clips}",
            font=font,
            fontsize=font_size,
            color="black",
            size=(video_width * 3 / 4, None),
            method='caption',
            align="north",
        ).set_duration(concatenated_clip.duration).set_start(0).set_position((160, 1100))



        final_composition = CompositeVideoClip([
            concatenated_clip,
            total_clips_text,
        ])



        # Check if the folder exists, and create it if it doesn't
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Specify the complete path to the final output file
        final_output_filename = os.path.join(folder_name, f"final_video_{timestamp}.mp4")

        # Write the concatenated clip to the file in the specified folder
        final_composition.write_videofile(final_output_filename, codec='libx264', audio_codec='aac', fps=24)

        for filename in generated_video_filenames:
            if filename != follow_clip:
                os.remove(filename)

        generated_video_filenames.clear()

    
    list_num -= 1

# Load the generated video clips
generated_clips = [VideoFileClip(filename) for filename in generated_video_filenames]

# Concatenate the generated clips
concatenated_clip = concatenate_videoclips(generated_clips)

# Write the concatenated clip to a file
final_output_filename = os.path.join(folder_name, f"final_video_{timestamp}.mp4")
concatenated_clip.write_videofile(final_output_filename, codec='libx264', audio_codec='aac', fps=24)

for filename in generated_video_filenames:
    if filename != follow_clip:
        os.remove(filename)

generated_video_filenames.clear()
    
    
print("Text Finished")