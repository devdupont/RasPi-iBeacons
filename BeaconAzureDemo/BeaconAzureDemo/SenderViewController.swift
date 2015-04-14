//
//  SenderViewController.swift
//  BeaconAzureDemo
//
//  Created by Michael duPont on 4/7/15.
//  Copyright (c) 2015 Michael duPont. All rights reserved.
//

import UIKit
import CoreLocation
import CoreBluetooth

class SenderViewController: UIViewController, UIApplicationDelegate, CBPeripheralManagerDelegate
{
    
    //Note the different spacing
    //Most applications read this with or without spaces
    let uuidString = "E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 62"
    //But Apple uses a different method of spacing
    let uuid = NSUUID(UUIDString: "E20A39F4-73F5-4BC4-A12F-17D1AD07A962")
    let majorValue = 0
    let minorValue = 0
    let majorHex = "00 00"
    let minorHex = "00 00"
    let idString = "iPhone.Beacon"
    
    let serverLocation = "https://myservice.azure-mobile.net/"
    let serverApplicationKey = "applicationKey"
    
    var client: MSClient?
    var peripheralManager = CBPeripheralManager()
    var advertisedData = NSDictionary()
    var region: CLBeaconRegion?
    
    @IBOutlet weak var CIDLabel: UILabel!
    @IBOutlet weak var MajorLabel: UILabel!
    @IBOutlet weak var MinorLabel: UILabel!
    @IBOutlet weak var SendStatusLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        region = CLBeaconRegion(proximityUUID: uuid, major: CLBeaconMajorValue(majorValue), minor: CLBeaconMinorValue(minorValue), identifier: idString)
        client = MSClient(applicationURLString: serverLocation, applicationKey: serverApplicationKey)
        CIDLabel.text = uuidString
        MajorLabel.text = "\(majorValue)"
        MinorLabel.text = "\(minorValue)"
        println("Sender Loaded")
    }
    
    @IBAction func sendToServer() {
        println("Button Pressed")
        //Create new row item where column "uuid" is uuidString
        let item = ["uuid":uuidString+" "+majorHex+" "+minorHex]
        println("Sending: " + uuidString + " " + majorHex + " " + minorHex)
        if (self.client != nil) {
            println("Getting Table")
            SendStatusLabel.text = "Getting Table"
            //Fetch table "Beacons"
            let itemTable = client!.tableWithName("Item")
            println("Inserting new item")
            SendStatusLabel.text = "Inserting"
            //Insert new row into "Beacons"
            itemTable.insert(item) {
                (insertedItem, error) in
                if (error != nil) {
                    println("Error" + error.description);
                    self.SendStatusLabel.text = "Error"
                } else {
                    println("Item inserted")
                    self.SendStatusLabel.text = "Success"
                }
            }
        }
    }
    
    @IBAction func toggleBroadcast(sender: UISwitch) {
        if sender.on {
            advertisedData = region!.peripheralDataWithMeasuredPower(nil)
            peripheralManager = CBPeripheralManager(delegate: self, queue: nil, options: nil)
            println("iBeacon is up")
        } else {
            peripheralManager.stopAdvertising()
            println("iBeacon is down")
        }
    }
    
    func peripheralManagerDidUpdateState(peripheral: CBPeripheralManager!) {
        switch peripheral.state {
        case CBPeripheralManagerState.PoweredOn:
            self.peripheralManager.startAdvertising(self.advertisedData as [NSObject : AnyObject])
            println("Powered On State")
        case CBPeripheralManagerState.PoweredOff:
            self.peripheralManager.stopAdvertising()
            println("Powered Off State")
        default: break
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillDisappear(animated: Bool) {
        self.peripheralManager.stopAdvertising()
        println("Stopping")
    }

}
