# Sound Bytes

Sound Bytes is an app similar to Twitter or Instagram Stories.
Users will upload "sound bites", 3 second to 2 minute audio clips.
These audio clips can contain anything, them talking, parts of songs, or a short book/magazine review, to name a few examples.

## Current Progress

The following is a list of what has been completed, what is being worked on, and what is planned in the future.
Items in **bold** have been completed.
Items in plain text are in progress.
Items in *italics* are planned.

* AWS Lambda
  - **Upload an audio file to AWS S3.**
  - **Upload audio file metadata to AWS DynamoDB.**
  - **Test audio file length to make sure it's between 3 and 120 seconds.**
  - **Get an audio file uplaod from a client.**
  - **Create a user database, and logins for them.**
  - *Make "captions" or computer generated text for each audio file.*
  - *Use the "captions" from each audio file to select preferred audio files for users.*
* *Application*
  - *Create landing page and icons.*
  - *Create login page for user.*
  - *Store login credentials in phone for a smother user exprience.*
  - *Design basic user interface of "list" of sound bites, and a recording button.*
  - *Record audio from the phone and send it to the AWS Lambda.*
  - *Get recording audio clips based on the user from the AWS Lambda.*

## Getting Started

There are two parts to Sound Bytes.
The front-end, or the application.
This is written in Android Studio, with plans to write for iOS.
And the back-end, or the server-side.
This uses Amazon Web Service's (AWS) lambdas, with Python.

If you want to experiment with the front-end download this repository and open the app in Android Studio.
If you want to experiment with the back-end download this repository and upload it to an AWS lambda.

### Prerequisites and Installing

##### Front-End

Using Android Studio; first install Android Studio from the [offical website](1).
Then open the Application located in the `SoundBytesApplication` folder.
This will open the Sound Bytes app, which you may play with as much as you'd like.

##### Back-End

The back-end uses [Serverless](2) with AWS lambdas.
First to install Serverless you need [Node.JS](3).
To install Node.JS, go to their [download page](4), and download the version you want, and follow the install instructions there.
To install Serverless follow their [instructions here](5), or run the following command.

```
npm install -g serverless
```

Then run `serverless --version` to make sure it's installed.
The back-end can be found in the `handler` folder.

## Built With

* [AWS Lambda](6) - The back-end execution
* [Serverless](2) - Tool to help with AWS Lambdas
* [Python](7) - Used to write the AWS Lambda
* [Android Studio](1) - Used to create the Application

## Contributing

If you would like to Contribute to this project, please do.
It's open source for a reason after all.
Simply submit a Pull Request or Issue here on Github.

## Authors

* **Preston Hager** - *Lead Programmer* - [Github Profile](https://github.com/PrestonHager)
* **Jonathan Hager** - *Solution Architect* - [Github Profile](https://github.com/JonathanHager)

Also see the list of [contributors](https://github.com/PrestonHager/SoundBytes/blob/master/CONTRIBUTORS.md) who participated in this project.

## License

This project is licensed under the GNU General Public License v3.0, see the [LICENSE](https://github.com/PrestonHager/SoundBytes/blob/master/LICENSE) file for details.

[1]: https://developer.android.com/studio/
[2]: https://serverless.com
[3]: https://nodejs.org/en/
[4]: https://nodejs.org/en/download/
[5]: https://serverless.com/framework/docs/providers/aws/guide/installation/
[6]: https://aws.amazon.com/lambda/
[7]: https://www.python.org
