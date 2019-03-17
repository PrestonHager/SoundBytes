BODY_FAIL = """<h2 style="display:inline-block">Sound Bytes Verify Email</h2>
<h2 style="margin-left:8px;color:red;display:inline-block"> Failure</h2>
<p>The link did not have, or had an invalid user token.
Please try clicking the link in your email, or click re-verify within the app.</p>
"""
BODY_SUCCESS = """<p>Please enable scripts to redirect.
If you don't click <a href="https://piprograms.pythonanywhere.com/soundbytes/verify?u=true">this link.</a></p>
<script>
var alink = document.createElement("<a href="https://piprograms.pythonanywhere.com/soundbytes/verify?u=true" />");
document.body.append(alink);
alink.click();
</script>
"""

RESPONSE_FAILURE = {
    "statusCode": 400,
    "headers": {
        "Content-Type": "text/html"
    },
    "body": "<html><head><title>Sound Bytes Verify Email</title></head><body>{body}</body></html>".format(body=BODY_FAIL)
}
RESPONSE_SUCCESS = {
    "statusCode": 200,
    "headers": {
        "Content-Type": "text/html"
    },
    "body": "<html><head><title>Sound Bytes Verify Email</title></head><body>{body}</body></html>".format(body=BODY_SUCCESS)
}
