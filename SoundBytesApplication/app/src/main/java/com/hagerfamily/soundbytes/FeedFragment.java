package com.hagerfamily.soundbytes;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import static android.content.Context.MODE_PRIVATE;

public class FeedFragment extends Fragment {

    private Context context;
    private LoginManager loginManager;
    private ServerRequester requester;
    private FeedAdapter userFeedAdapter;
    private SwipeRefreshLayout userFeedRefreshLayout;
    private String urlGetBites;

    public FeedFragment() {}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // set url variable.
        urlGetBites = getString(R.string.url_get_bites);
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
        Log.i("SoundBytesFeed","Refreshing feed data.");
        userFeedAdapter.updatePosts(getUserFeed());
        userFeedAdapter.notifyDataSetChanged();
        userFeedRefreshLayout.setRefreshing(false);
    }

    private JSONArray getUserFeed() {
        JSONObject params = new JSONObject();
        try { params.put("tkn", loginManager.clientTokensSp.getString("AccessToken", "null")); } catch (JSONException ignored) {}
        JSONObject response = requester.GetRequest(params, urlGetBites);
        Log.i("SoundBytesFeed", "Response was "+response.toString());
        // TODO: make raise error if times out.
        try {
            return response.getJSONArray("all_posts");
        } catch (JSONException e) {
            e.printStackTrace();
            Toast.makeText(context, R.string.error_feed_update, Toast.LENGTH_LONG).show();
            userFeedRefreshLayout.setRefreshing(false);
            return new JSONArray();
        }
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        this.context = context;
        requester = new ServerRequester(context);
    }
}
