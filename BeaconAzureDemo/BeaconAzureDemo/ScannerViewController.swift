//
//  ScannerViewController.swift
//  BeaconAzureDemo
//
//  Created by Michael duPont on 4/7/15.
//  Copyright (c) 2015 Michael duPont. All rights reserved.
//

import UIKit
import CoreLocation

class ScannerViewController: UIViewController, CLLocationManagerDelegate
{
    
    let uuidToLookFor = NSUUID(UUIDString: "E20A39F4-73F5-4BC4-A12F-17D1AD07A961")
    let idString = "My Python Beacon"
    
    let locationManager = CLLocationManager()
    var region: CLBeaconRegion?
    
    let colors = [
        0: UIColor.blueColor(),
        1: UIColor.yellowColor(),
        2: UIColor.greenColor(),
        3: UIColor.redColor()
    ]
    
    let status = [
        0: "Feeling Blue?",
        1: "Darude Sandstorm by Darude",
        2: "Green with Hulk",
        3: "I am Iron Man"
    ]
    
    @IBOutlet weak var statusLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        locationManager.delegate = self
        region = CLBeaconRegion(proximityUUID: uuidToLookFor, identifier: idString)
        if (CLLocationManager.authorizationStatus() != CLAuthorizationStatus.AuthorizedWhenInUse) {
            locationManager.requestWhenInUseAuthorization()
        }
        locationManager.startRangingBeaconsInRegion(region)
        self.view.backgroundColor = UIColor.whiteColor()
        self.statusLabel.text = "Scanning..."
    }
    
    func locationManager(manager: CLLocationManager!, didRangeBeacons beacons: [AnyObject]!, inRegion region: CLBeaconRegion!) {
        let knownBeacons = beacons.filter{ $0.proximity != CLProximity.Unknown }
        println(knownBeacons)
        if (knownBeacons.count > 0) {
            let closestBeacon = knownBeacons[0] as! CLBeacon
            let beaconMinorValue = closestBeacon.minor.integerValue
            self.view.backgroundColor = self.colors[beaconMinorValue]!
            self.statusLabel.text = self.status[beaconMinorValue]
        }else {
            self.view.backgroundColor = UIColor.whiteColor()
            self.statusLabel.text = "Scanning..."
        }
    }
    
    override func viewWillDisappear(animated: Bool) {
        locationManager.stopRangingBeaconsInRegion(region)
        println("Stopping")
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        locationManager.stopRangingBeaconsInRegion(region)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}
