package com.hagerfamily.soundbytes;

import android.support.v4.app.FragmentActivity;
import android.support.v4.view.ViewPager;
import android.os.Bundle;

public class MainActivity extends FragmentActivity{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        MainActivityPagerAdapter activityPagerAdapter = new MainActivityPagerAdapter(getSupportFragmentManager());
        ViewPager activityViewPager = findViewById(R.id.pager);
        activityViewPager.setAdapter(activityPagerAdapter);
    }

}
