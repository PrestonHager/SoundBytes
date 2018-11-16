package com.hagerfamily.soundbytes;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

class FeedAdapter extends RecyclerView.Adapter<FeedAdapter.FeedViewHolder> {

    private ArrayList<Post> postsList = new ArrayList<>();

    static class FeedViewHolder extends RecyclerView.ViewHolder {
        View view;
        TextView titleTextView, bodyTextView;
        FeedViewHolder(View v) {
            super(v);
            view = v;
            titleTextView = v.findViewById(R.id.postTitle);
            bodyTextView = v.findViewById(R.id.postBody);
        }
    }

    FeedAdapter() {}

    private void updatePost(JSONObject jsonPost) {
        try {
            Post post = new Post(jsonPost.getString("t"), jsonPost.getString("b"));
            postsList.add(0, post);
            this.notifyItemInserted(0);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    void updatePosts (JSONArray posts) {
        postsList.clear();
        this.notifyDataSetChanged();
        insertPosts(posts);
    }

    private void insertPosts(JSONArray posts) {
        try {
            for (int i = 0; i < posts.length(); i++) {
                JSONObject jsonPost = posts.getJSONObject(i);
                updatePost(jsonPost);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Create new views (invoked by the layout manager)
    @Override
    public FeedAdapter.FeedViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.post_fragment, parent, false);
        return new FeedViewHolder(v);
    }

    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(FeedViewHolder holder, int position) {
        String postTitle = postsList.get(position).title.toString();
        String postBody = postsList.get(position).body.toString();

        holder.titleTextView.setText(postTitle);
        holder.bodyTextView.setText(postBody);
    }

    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return postsList.size();
    }
}
