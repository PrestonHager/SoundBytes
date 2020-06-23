//
//  AudioController.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/4/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation
import Combine
import AVFoundation

class AudioController: NSObject, ObservableObject, AVAudioPlayerDelegate, AVAudioRecorderDelegate {
    var audioPlayer: AVAudioPlayer!
    var audioRecorder: AVAudioRecorder!
    var audioSession: AVAudioSession!

    let objectWillChange = PassthroughSubject<AudioController, Never>()
    var hasRecordingPermission = false

    var playing = false {
        didSet {
            objectWillChange.send(self)
        }
    }
    var recording = false {
        didSet {
            objectWillChange.send(self)
        }
    }
        
    // An array to hold all the recordings.
    var recordings = [Recording]()
    
    override init() {
        super.init()
        audioSession = AVAudioSession.sharedInstance()
        let audioSessionOptions: AVAudioSession.CategoryOptions = [
            .allowBluetooth,
            .allowBluetoothA2DP,
            .allowAirPlay
        ]
        
        do {
            try audioSession.setCategory(.playAndRecord, mode: .default, options: audioSessionOptions)
            try audioSession.setActive(true)
            switch audioSession.recordPermission {
            case AVAudioSessionRecordPermission.granted:
                hasRecordingPermission = true
                break
            case AVAudioSessionRecordPermission.denied:
                break
            case AVAudioSessionRecordPermission.undetermined:
                AVAudioSession.sharedInstance().requestRecordPermission({ granted in
                    if (granted) {
                        self.hasRecordingPermission = true
                    }
                })
            default:
                break
            }
        } catch {
            print("Failed to set up recording session")
        }
        
        self.fetchRecordings()
    }
    
    func play(recording: Recording) -> Bool {
        do {
            audioPlayer = try AVAudioPlayer(contentsOf: recording.fileURL)
            audioPlayer.delegate = self
            audioPlayer.setVolume(50, fadeDuration: TimeInterval(0))
            audioPlayer.prepareToPlay()
            audioPlayer.play()
            playing = true
        } catch {
            print( "Could not find file")
        }
        
        // Return whether or not playing was successful.
        return playing
    }
    
    func record() -> Bool {
        // First, check to see if we don't have permission.
        if (!hasRecordingPermission) {
            return false
        }
        
        // Get the path for the file and make an audiofile name.
        let documentPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let audioFilename = documentPath.appendingPathComponent("\(Date().toString(dateFormat: "dd-MM-YY 'at' HH:mm:ss")).m4a")
        
        // The settings for the recording file.
        let settings = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 12000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        // Finally, we get to record something!
        do {
            audioRecorder = try AVAudioRecorder(url: audioFilename, settings: settings)
            audioRecorder.delegate = self
            audioRecorder.prepareToRecord()
            audioRecorder.record()
            recording = true
        } catch {
            print("Could not start recording")
        }
        
        // Return whether or not recording was successful.
        return recording
    }
    
    func stop() {
        if recording {
            audioRecorder.stop()
            recording = false
            self.fetchRecordings()
        } else if playing {
            audioPlayer.stop()
            playing = false
        }
    }
    
    func fetchRecordings() {
        recordings.removeAll()
        
        // The file stuff.
        let fileManager = FileManager.default
        let documentDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let directoryContents = try! fileManager.contentsOfDirectory(at: documentDirectory, includingPropertiesForKeys: nil)
        // Get each audio file and add it to the list of recordings.
        for audio in directoryContents {
            let audioName: String = audio.lastPathComponent
            let recording = Recording(name: audioName, fileURL: audio, createdAt: getCreationDate(for: audio))
            recordings.append(recording)
        }
        
        // Sort the recordings in order of creation.
        recordings.sort(by: { $0.createdAt.compare($1.createdAt) == .orderedAscending})
        objectWillChange.send(self)
    }
    
    // TODO: polish
    func deleteRecording(fileURL: URL) {
        let fileManager = FileManager.default
        do {
            try fileManager.removeItem(at: fileURL)
        } catch {
            print("Failed to delete file.")
        }
    }
    
    // Get a Date from the recordings file.
    func getCreationDate(for file: URL) -> Date {
        if let attributes = try? FileManager.default.attributesOfItem(atPath: file.path) as [FileAttributeKey: Any],
            let creationDate = attributes[FileAttributeKey.creationDate] as? Date {
            return creationDate
        } else {
            return Date()
        }
    }
    
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        if flag {
            NotificationCenter.default.post(name: Notification.Name("audioPlayerDidFinishPlayingSuccessfully"), object: nil)
        } else {
            NotificationCenter.default.post(name: Notification.Name("audioPlayerDidFinishPlayingUnsuccessfully"), object: nil)
        }
        // Ensure all variables are set back to defaults.
        playing = false
        audioPlayer = nil
    }
    func audioPlayerDecodeErrorDidOccur(_ player: AVAudioPlayer, error: Error?) {
        print("Audio Player Decode Error!")
        audioPlayer = nil
    }
    
    func audioRecorderDidFinishRecording(_ recorder: AVAudioRecorder, successfully flag: Bool) {
        if flag {
            NotificationCenter.default.post(name: Notification.Name("audioRecorderDidFinishPlayingSuccessfully"), object: nil)
        } else {
            NotificationCenter.default.post(name: Notification.Name("audioRecorderDidFinishPlayingUnsuccessfully"), object: nil)
        }
        // Ensure all variables are set back to defaults.
        recording = false
        audioRecorder = nil
    }
    func audioRecorderEncodeErrorDidOccur(_ recorder: AVAudioRecorder, error: Error?) {
        print("Audio Recorder Encode Error!")
        audioRecorder = nil
    }
}
