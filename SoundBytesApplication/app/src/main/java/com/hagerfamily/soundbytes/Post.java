package com.hagerfamily.soundbytes;

import android.provider.MediaStore;

class Post {

    CharSequence title;
    CharSequence body;
    MediaStore.Audio audio;

    Post(CharSequence title, CharSequence body) {
        this.title = title;
        this.body = body;
    }

    Post(CharSequence title, CharSequence body, MediaStore.Audio audio) {
        this.title = title;
        this.body = body;
        this.audio = audio;
    }

}
