package com.hagerfamily.soundbytes;

import android.content.res.Resources;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;

class MainActivityPagerAdapter extends FragmentPagerAdapter {
    MainActivityPagerAdapter(FragmentManager supportFragmentManager) {
        super(supportFragmentManager);
    }

    @Override
    public Fragment getItem(int i) {
        Fragment fragment = new MainActivityFragment();
        switch (i) {
            case 0:
                fragment = new FeedFragment();
        }
        return fragment;
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
