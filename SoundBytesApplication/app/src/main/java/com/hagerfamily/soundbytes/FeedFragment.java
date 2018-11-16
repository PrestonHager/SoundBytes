package com.hagerfamily.soundbytes;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.widget.GridLayoutManager;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.hagerfamily.soundbytes.dummy.DummyContent;
import com.hagerfamily.soundbytes.dummy.DummyContent.DummyItem;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.List;

import static android.content.Context.MODE_PRIVATE;

public class FeedFragment extends Fragment {

    private Context context;
    private LoginManager loginManager;
    private ServerRequester requester = new ServerRequester();
    private FeedAdapter userFeedAdapter;
    private SwipeRefreshLayout userFeedRefreshLayout;

    public FeedFragment() {}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.feed_fragment, container, false);

        // Set the adapter
        RecyclerView userFeed = view.findViewById(R.id.userFeed);
        userFeed.setHasFixedSize(false);
        userFeedAdapter = new FeedAdapter();
        LinearLayoutManager userFeedLayoutManager = new LinearLayoutManager(context);
        userFeedLayoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        userFeed.setLayoutManager(userFeedLayoutManager);
        userFeed.setAdapter(userFeedAdapter);

        userFeedRefreshLayout = view.findViewById(R.id.userFeedRefreshLayout);
        userFeedRefreshLayout.setOnRefreshListener(
                new SwipeRefreshLayout.OnRefreshListener() {
                    @Override
                    public void onRefresh() {
                        updateUserFeed();
                    }
                }
        );

        loginManager = new LoginManager(context.getSharedPreferences("ClientTokens", MODE_PRIVATE), context.getSharedPreferences("Login", MODE_PRIVATE));

        // finally update the user feed.
        updateUserFeed();

        return view;
    }

    private void updateUserFeed() {
        // refresh the recycler view, userFeed.
        Log.i("SoundBytesFeed","Refreshing.");
        try {
            userFeedAdapter.updatePosts(getUserFeed());
            userFeedAdapter.notifyDataSetChanged();
            userFeedRefreshLayout.setRefreshing(false);
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(context, R.string.errorFeedUpdate, Toast.LENGTH_LONG).show();
            userFeedRefreshLayout.setRefreshing(false);
        }
    }

    private JSONArray getUserFeed() throws JSONException {
        return new JSONArray().put(new JSONObject().put("t", "Test 123!").put("b", "Hello There! This is a test post with a test body paragraph."));
//        JSONObject json = new JSONObject();
//        json.put("username", loginManager.loginSp.getString("Username", ""));
//        json.put("id", loginManager.clientTokensSp.getString("AccessToken", ""));
//        return requester.JSONRequest(json, "https://faidg1ey0l.execute-api.us-west-2.amazonaws.com/prod/get-bites").getJSONArray("all_posts");
        // TODO: make raise error if times out.
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        this.context = context;
    }
}
