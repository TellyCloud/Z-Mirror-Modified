mirror = """
<b>Send link along with command line or </b>

/cmd link

<b>By replying to link/file</b>:

/cmd -n new name -e -up upload destination

<b>NOTE:</b>
1. Commands that start with <b>qb</b> are ONLY for torrents.

<b>Join: @Z_Mirror</b>
"""

yt = """
<b>Send link along with command line</b>:

/cmd link

<b>By replying to link</b>:

/cmd -n new name -z password -opt x:y|x1:y1

Check all supported <a href='https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md'>SITES</a>
Check all yt-dlp API options from this <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L184'>FILE</a> or use this <a href='https://t.me/mltb_official_channel/177'>script</a> to convert CLI arguments to API options.

<b>Join: @Z_Mirror</b>
"""

clone = """
Send Gdrive link or rclone path along with command or by replying to the link/rc_path by command.

Use -sync to use sync method in rclone.

Example: /cmd rcl/rclone_path -up rcl/rclone_path/rc -sync

<b>Join: @Z_Mirror</b>
"""

new_name = """
<b>New Name</b>: -n

/cmd link -n new name
Note: Doesn't work with torrents

<b>Join: @Z_Mirror</b>
"""

multi_link = """
<b>Multi links only by replying to the first link/file</b>: -i

/cmd -i 10(number of links/files)

<b>Join: @Z_Mirror</b>
"""

same_dir = """
<b>Multi links within the same upload directory only by replying to the first link/file</b>: -m

/cmd -i 10(number of links/files) -m folder name (multi message)
/cmd -b -m folder name (bulk-message/file)

<b>Join: @Z_Mirror</b>
"""

thumb = """
<b>Thumbnail for the current task</b>: -t

/cmd link -t tg-message-link(doc or photo)

<b>Join: @Z_Mirror</b>
"""

split_size = """
<b>Split size for the current task</b>: -sp

/cmd link -sp (500mb or 2gb or 4000000000)
Note: Only mb and gb are supported or write in bytes without unit!

<b>Join: @Z_Mirror</b>
"""

upload = """
<b>Upload Destination</b>: -up

/cmd link -up rcl/gdl (To select rclone config/token.pickle, remote & path/ gdrive id or Tg id/username)
You can directly add the upload path: -up remote:dir/subdir or -up (Gdrive_id) or -up id/username
If DEFAULT_UPLOAD is `rc` then you can pass up: `gd` to upload using gdrive tools to GDRIVE_ID.
If DEFAULT_UPLOAD is `gd` then you can pass up: `rc` to upload to RCLONE_PATH.

If you want to add path or gdrive manually from your config/token (uploaded from usetting) add mrcc: for rclone and mtp: before the path/gdrive_id without space.
/cmd link -up mrcc:main:dump or -up mtp:gdrive_id or -up b:id/@username/pm(leech by bot) or -up u:id/@username(leech by user) or -up m:id/@username(mixed leech)

In case you want to specify whether using token.pickle or service accounts you can add tp:gdrive_id or sa:gdrive_id or mtp:gdrive_id.
DEFAULT_UPLOAD has no effect on leech cmds.

<b>Join: @Z_Mirror</b>
"""

user_download = """
<b>User Download</b>: link

/cmd tp:link to download using owner token.pickle in case service account enabled.
/cmd sa:link to download using service account in case service account disabled.
/cmd tp:gdrive_id to download using token.pickle and file_id in case service account enabled.
/cmd sa:gdrive_id to download using service account and file_id in case service account disabled.
/cmd mtp:gdrive_id or mtp:link to download using user token.pickle uploaded from usetting
/cmd mrcc:remote:path to download using user rclone config uploaded from usetting

<b>Join: @Z_Mirror</b>
"""

rcf = """
<b>Rclone Flags</b>: -rcf

/cmd link|path|rcl -up path|rcl -rcf --buffer-size:8M|--drive-starred-only|key|key:value
This will override all other flags except --exclude.
Check here all <a href='https://rclone.org/flags/'>RcloneFlags</a>.

<b>Join: @Z_Mirror</b>
"""

bulk = """
<b>Bulk Download</b>: -b

Bulk can be used by text message and by replying to a text file containing links separated by a new line.
You can use it only by replying to a message(text/file).
Example:
link1 -n new name -up remote1:path1 -rcf |key:value|key:value
link2 -z -n new name -up remote2:path2
link3 -e -n new name -up remote2:path2
Reply to this example by this cmd -> /cmd -b(bulk) or /cmd -b -m folder name
You can set the start and end of the links from the bulk like seed, with -b start:end or only end by -b :end or only start by -b start.
The default start is from zero(first link) to infinity.

<b>Join: @Z_Mirror</b>
"""

rlone_dl = """
<b>Rclone Download</b>:

Treat rclone paths exactly like links
/cmd main:dump/ubuntu.iso or rcl(To select config, remote, and path)
Users can add their own rclone from user settings
If you want to add a path manually from your config add mrcc: before the path without space
/cmd mrcc:main:dump/ubuntu.iso

<b>Join: @Z_Mirror</b>
"""

extract_zip = """
<b>Extract/Zip</b>: -e -z

/cmd link -e password (extract password protected)
/cmd link -z password (zip password protected)
/cmd link -z password -e (extract and zip password protected)
Note: When both extract and zip are added with cmd, it will extract first and then zip, so always extract first.

<b>Join: @Z_Mirror</b>
"""

join = """
<b>Join Splitted Files</b>: -j

This option will only work before extract and zip, so mostly it will be used with -m argument (samedir)
By Reply:
/cmd -i 3 -j -m folder name
/cmd -b -j -m folder name
If you have a link(folder) that has split files:
/cmd link -j

<b>Join: @Z_Mirror</b>
"""

tg_links = """
<b>TG Links</b>:

Treat links like any direct link
Some links need user access so make sure you have added USER_SESSION_STRING for it.
Three types of links:
Public: https://t.me/channel_name/message_id
Private: tg://openmessage?user_id=xxxxxx&message_id=xxxxx
Super: https://t.me/c/channel_id/message_id
Range: https://t.me/channel_name/first_message_id-last_message_id
Range Example: tg://openmessage?user_id=xxxxxx&message_id=555-560 or https://t.me/channel_name/100-150
Note: Range link will work only by replying cmd to it.

<b>Join: @Z_Mirror</b>
"""

sample_video = """
<b>Sample Video</b>: -sv

Create a sample video for one video or a folder of videos.
/cmd -sv (it will take the default values which are 60sec sample duration and part duration is 4sec).
You can control those values. Example: /cmd -sv 70:5(sample-duration:part-duration) or /cmd -sv :5 or /cmd -sv 70.

<b>Join: @Z_Mirror</b>
"""

screenshot = """
<b>Screenshots</b>: -ss

Create up to 10 screenshots for one video or a folder of videos.
/cmd -ss (it will take the default values which are 10 photos).
You can control this value. Example: /cmd -ss 6.

<b>Join: @Z_Mirror</b>
"""

seed = """
<b>Bittorrent Seed</b>: -d

/cmd link -d ratio:seed_time or by replying to file/link
To specify ratio and seed time add -d ratio:time.
Example: -d 0.7:10 (ratio and time) or -d 0.7 (only ratio) or -d :10 (only time) where time is in minutes.

<b>Join: @Z_Mirror</b>
"""

zip_arg = """
<b>Zip</b>: -z password

/cmd link -z (zip)
/cmd link -z password (zip password protected)

<b>Join: @Z_Mirror</b>
"""

qual = """
<b>Quality Buttons</b>: -s

In case default quality is added from yt-dlp options using format option and you need to select quality for specific link or links with multi links feature.
/cmd link -s

<b>Join: @Z_Mirror</b>
"""

yt_opt = """
<b>Options</b>: -opt

/cmd link -opt playliststart:^10|fragment_retries:^inf|matchtitle:S13|writesubtitles:true|live_from_start:true|postprocessor_args:{"ffmpeg": ["-threads", "4"]}|wait_for_video:(5, 100)
Note: Add `^` before integer or float, some values must be numeric and some string.
Like playlist_items:10 works with string, so no need to add `^` before the number but playlistend works only with integer so you must add `^` before the number like example above.
You can add tuple and dict also. Use double quotes inside dict.

<b>Join: @Z_Mirror</b>
"""

convert_media = """
<b>Convert Media</b>: -ca -cv
/cmd link -ca mp3 -cv mp4 (convert all audios to mp3 and all videos to mp4)
/cmd link -ca mp3 (convert all audios to mp3)
/cmd link -cv mp4 (convert all videos to mp4)
/cmd link -ca mp3 + flac ogg (convert only flac and ogg audios to mp3)
/cmd link -cv mp4 - webm flv (convert all videos to mp4 except webm and flv)

<b>Join: @Z_Mirror</b>
"""

force_start = """
<b>Force Start</b>: -f -fd -fu
/cmd link -f (force download and upload)
/cmd link -fd (force download only)
/cmd link -fu (force upload directly after download finishes)

<b>Join: @Z_Mirror</b>
"""

gdrive = """
<b>Gdrive</b>: link
If DEFAULT_UPLOAD is `rc` then you can pass up: `gd` to upload using gdrive tools to GDRIVE_ID.
/cmd gdriveLink or gdl or gdriveId -up gdl or gdriveId or gd
/cmd tp:gdriveLink or tp:gdriveId -up tp:gdriveId or gdl or gd (to use token.pickle if service account enabled)
/cmd sa:gdriveLink or sa:gdriveId -p sa:gdriveId or gdl or gd (to use service account if service account disabled)
/cmd mtp:gdriveLink or mtp:gdriveId -up mtp:gdriveId or gdl or gd(if you have added upload gdriveId from usetting) (to use user token.pickle that uploaded by usetting)

<b>Join: @Z_Mirror</b>
"""

rclone_cl = """
<b>Rclone</b>: path
If DEFAULT_UPLOAD is `gd` then you can pass up: `rc` to upload to RCLONE_PATH.
/cmd rcl/rclone_path -up rcl/rclone_path/rc -rcf flagkey:flagvalue|flagkey|flagkey:flagvalue
/cmd rcl or rclonePath -up rclonePath or rc or rcl
/cmd mrcc:rclonePath -up rcl or rc(if you have added rclone path from usetting) (to use user config)

<b>Join: @Z_Mirror</b>
"""

name_sub = """
<b>Name Substitution</b>: -ns
/cmd link -ns tea : coffee : s|ACC :  : s|mP4
This will affect all files. Format: wordToReplace : wordToReplaceWith : sensitiveCase
1. tea will get replaced by coffee with sensitive case because I have added `s` last of the option.
2. ACC will get removed because I have added nothing between to replace with sensitive case because I have added `s` last of the option.
3. mP4 will get removed because I have added nothing to replace with

<b>Join: @Z_Mirror</b>
"""

mixed_leech = """
<b>Mixed Leech</b>: -ml
/cmd link -ml (leech by user and bot session with respect to size)

<b>Join: @Z_Mirror</b>
"""

YT_HELP_DICT = {
    "main": yt,
    "New-Name": f"{new_name}\nNote: Don't add file extension",
    "Zip": zip_arg,
    "Quality": qual,
    "Options": yt_opt,
    "Multi-Link": multi_link,
    "Same-Directory": same_dir,
    "Thumb": thumb,
    "Split-Size": split_size,
    "Upload-Destination": upload,
    "Rclone-Flags": rcf,
    "Bulk": bulk,
    "Sample-Video": sample_video,
    "Screenshot": screenshot,
    "Convert-Media": convert_media,
    "Force-Start": force_start,
    "Name-Substitute": name_sub,
    "Mixed-Leech": mixed_leech,
}

MIRROR_HELP_DICT = {
    "main": mirror,
    "New-Name": new_name,
    "DL-Auth": "<b>Direct link authorization</b>: -au -ap\n\n/cmd link -au username -ap password",
    "Headers": "<b>Direct link custom headers</b>: -h\n\n/cmd link -h key: value key1: value1",
    "Extract/Zip": extract_zip,
    "Select-Files": "<b>Bittorrent File Selection</b>: -s\n\n/cmd link -s or by replying to file/link",
    "Torrent-Seed": seed,
    "Multi-Link": multi_link,
    "Same-Directory": same_dir,
    "Thumb": thumb,
    "Split-Size": split_size,
    "Upload-Destination": upload,
    "Rclone-Flags": rcf,
    "Bulk": bulk,
    "Join": join,
    "Rclone-DL": rlone_dl,
    "Tg-Links": tg_links,
    "Sample-Video": sample_video,
    "Screenshot": screenshot,
    "Convert-Media": convert_media,
    "Force-Start": force_start,
    "User-Download": user_download,
    "Name-Substitute": name_sub,
    "Mixed-Leech": mixed_leech,
}

CLONE_HELP_DICT = {
    "main": clone,
    "Multi-Link": multi_link,
    "Bulk": bulk,
    "Gdrive": gdrive,
    "Rclone": rclone_cl,
}

RSS_HELP_MESSAGE = """
Use this format to add feed url:
Title1 link (required)
Title2 link -c cmd -inf xx -exf xx
Title3 link -c cmd -d ratio:time -z password

-c command -up mrcc:remote:path/subdir -rcf --buffer-size:8M|key|key:value
-inf For included words filter.
-exf For excluded words filter.
-stv true or false (sensitive filter)

Example: Title https://www.rss-url.com -inf 1080 or 720 or 144p|mkv or mp4|hevc -exf flv or web|xxx
This filter will parse links that its titles contain `(1080 or 720 or 144p) and (mkv or mp4) and hevc` and don't contain (flv or web) and xxx words. You can add whatever you want.

Another example: -inf  1080  or 720p|.web. or .webrip.|hvec or x264. This will parse titles that contain (1080 or 720p) and (.web. or .webrip.) and (hvec or x264). I have added space before and after 1080 to avoid wrong matching. If this `10805695` number in the title it will match 1080 if added 1080 without spaces after it.

Filter Notes:
1. | means and.
2. Add `or` between similar keys, you can add it between qualities or between extensions, so don't add a filter like this f: 1080|mp4 or 720|web because this will parse 1080 and (mp4 or 720) and web ... not (1080 and mp4) or (720 and web).
3. You can add `or` and `|` as much as you want.
4. Take a look at the title if it has a static special character after or before the qualities or extensions or whatever and use them in the filter to avoid wrong match.
Timeout: 60 sec.

<b>Join: @Z_Mirror</b>
"""

PASSWORD_ERROR_MESSAGE = """
<b>This link requires a password!</b>
- Insert <b>::</b> after the link and write the password after the sign.

<b>Example:</b> link::my password

<b>Join: @Z_Mirror</b>
"""
