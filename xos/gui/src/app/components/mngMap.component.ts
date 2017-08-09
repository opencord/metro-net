import {NgMap} from 'ngmap';
import {Subscription} from 'rxjs/Subscription';
import * as _ from 'lodash';

declare var google;

let self;

export class MngMap {

  static $inject = [
    'NgMap',
    'XosModelStore',
    'AppConfig',
    '$resource',
    'XosSidePanel',
    'XosModelDiscoverer',
    'ModelRest',
    'MapConfig',
  ];

  public unis = [];
  public elines = [];
  public cpilatlng = new Map();
  public paths = [];
  public bwps = [];
  public map;
  public panelOpen = false;
  public createMode = false;
  public canCreateEline = true;
  public eline;
  public current_uni;
  public mapStyles = [{'featureType': 'administrative', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#444444'}]}, {'featureType': 'landscape', 'elementType': 'all', 'stylers': [{'color': '#f2f2f2'}]}, {'featureType': 'poi', 'elementType': 'all', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'road', 'elementType': 'all', 'stylers': [{'saturation': -100}, {'lightness': 45}]}, {'featureType': 'road.highway', 'elementType': 'all', 'stylers': [{'visibility': 'simplified'}]}, {'featureType': 'road.arterial', 'elementType': 'labels.icon', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'transit', 'elementType': 'all', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'water', 'elementType': 'all', 'stylers': [{'color': '#9ce1fc'}, {'visibility': 'on'}]}];

  private uniSubscription: Subscription;
  private elineSubscription: Subscription;
  private bwpSubscription: Subscription;

  constructor(
    private NgMap: any,
    private XosModelStore: any,
    private AppConfig: any,
    private $resource: any,
    private XosSidePanel: any,
    private XosModelDiscoverer: any,
    private ModelRest: any,
    private MapConfig: any,
  ) {
    self = this;
  }

  $onInit() {
    this.NgMap.getMap().then(map => {
      this.map = map;
      this.uniSubscription = this.XosModelStore.query('UserNetworkInterface', '/metronet/usernetworkinterfaces/').subscribe(
        res => {
          this.unis = res;
          this.renderMap(map);
        }
      );
      this.elineSubscription = this.XosModelStore.query('ELine', '/metronet/elines/').subscribe(
        res => {
          this.elines = res;
          this.createPaths();
          this.renderMap(map);
        }
      );
      this.bwpSubscription = this.XosModelStore.query('BandwidthProfile', '/metronet/bandwidthprofiles/').subscribe(
        res => {
          this.bwps = res;
        }
      );
    });
  }

  $onDestroy() {
    if (this.uniSubscription) {
      this.uniSubscription.unsubscribe();
    }
  }

  public renderMap(map: NgMap) {

    let bounds = new google.maps.LatLngBounds();

    for (let i = 0; i < self.unis.length; i++) {
      self.unis[i].eline_start = false;
      let curr = JSON.parse(self.unis[i].latlng);
      this.cpilatlng.set(self.unis[i].cpe_id, curr);
      let latlng = new google.maps.LatLng(curr[0], curr[1]);
      bounds.extend(latlng);
    }
    map.setCenter(bounds.getCenter());
    map.fitBounds(bounds);

  }

  public createPaths() {
    this.elines.forEach((eline: any) => {
      let latlng_start = this.cpilatlng.get(eline.connect_point_1_id);
      let latlng_end = this.cpilatlng.get(eline.connect_point_2_id);
      eline.path = [latlng_start, latlng_end];
    });

  }

  public colorLine(eline_status : any) {
    let status = parseInt(eline_status, 10);
    switch (status) {
      case 0:
        return '#f39c12';
      case 1:
        return '#2ecc71';
      default:
        return '#e74c3c';
    }

  }

  public showUni(e: any, uni: any) {
    self.current_uni = uni;
    self.map.showInfoWindow('uni-info', this);
  }

  // do not display backend status or ID in create mode

  public elinePanel(e: any, eline: any, exists: boolean) {
    self.panelOpen = !self.panelOpen;
    if (exists) {
      self.eline = _.find(self.elines, {id: eline.id});
    }
    self.XosSidePanel.toggleComponent('elineSide', {eline: self.eline, bwplist: self.bwps, mng: self}, false);
    if (!self.panelOpen && self.createMode) {
      self.createMode = false;
      self.canCreateEline = true;
      self.current_uni.eline_start = false;
    }

  }

  public createConnection(uni: any) {
    return () => {
      self.canCreateEline = false;
      self.createMode = true;
      uni.eline_start = true;
      self.current_uni = uni;
      self.eline = {
        name: uni.name,
        uni1name: uni.name,
        connect_point_1_id: uni.cpe_id,
      };
      self.elinePanel({}, self.eline, false);
    };

  }

  public finishConnection(uni: any) {
    self.eline.connect_point_2_id = uni.cpe_id;
    if (self.eline.name === self.eline.uni1name) {
      self.eline.name = self.eline.name + uni.name;
    }
    delete self.eline.uni1name;
    const resource = this.ModelRest.getResource('/metronet/elines/');
    let res = new resource({});
    for (let attr in self.eline) {
      if (true) {
        res[attr] = self.eline[attr];
      }

    }
    self.eline = res;
  }

}

export const mngMap: angular.IComponentOptions = {
  template: require('./mngMap.component.html'),
  controllerAs: 'vm',
  controller: MngMap,
};
