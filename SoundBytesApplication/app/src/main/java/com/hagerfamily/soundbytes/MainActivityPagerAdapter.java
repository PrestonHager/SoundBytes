package com.hagerfamily.soundbytes;

import android.content.res.Resources;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;

class MainActivityPagerAdapter extends FragmentPagerAdapter {
    MainActivityPagerAdapter(FragmentManager supportFragmentManager) {
        super(supportFragmentManager);
    }

    @Override
    public Fragment getItem(int i) {
        switch (i) {
            case 0:
                return new FeedFragment();
            case 1:
                return new NewPostFragment();
            case 2:
                return new SettingsFragment();
        }
        return new SplashActivityFragment();
    }

    @Override
    public int getCount() {
        return 3;
    }

    @Override
    public CharSequence getPageTitle(int position) {
        switch (position) {
            case 0:
                return Resources.getSystem().getString(R.string.title_activity_main);
            case 1:
                return Resources.getSystem().getString(R.string.title_activity_new);
            case 2:
                return Resources.getSystem().getString(R.string.title_activity_settings);
        }
        return null;
    }
}
