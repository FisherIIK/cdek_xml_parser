# -*- coding: utf-8 -*-
import csv
import requests
import xml.etree.ElementTree as ET
import sys


def createXMLFromWeb():
    url = 'http://integration.cdek.ru/pvzlist/v1/xml'
    print("in create xml")
    resp = requests.get(url)
    with open('cdek.xml', 'wb') as file:
        file.write(resp.content)


def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    stationitems = []
    print("in parse xml")
    for item in root.findall('./Pvz'):
        stations = {}
        #print(item.attrib['Code'])
        stations['Code'] = item.attrib['Code']
        stations['FullAddress'] = item.attrib['FullAddress']
        stations['MetroStation'] = item.attrib['MetroStation']
        print(stations)
        stationitems.append(stations)
    return stationitems


def xmlFiletoCSV(stations, filename):
    fields = ['Code', 'FullAddress', 'MetroStation']
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(stations)


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    createXMLFromWeb()
    stations = parseXML('cdek.xml')
    xmlFiletoCSV(stations, 'stationList.csv')


if __name__ == "__main__":
    main()