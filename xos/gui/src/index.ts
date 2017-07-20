/// <reference path="../typings/index.d.ts" />
import * as angular from 'angular';

import 'angular-ui-router';
import 'angular-resource';
import 'angular-cookies';

import 'ngmap';

import routesConfig from './routes';
import {mngMap} from './app/components/mngMap.component';
import {elineSide} from './app/components/eline-side.component';

angular.module('metro-net-gui', [
    'ui.router',
    'app',
    'ngMap'
  ])
  .config(routesConfig)
  .component('mngMap', mngMap)
  .component('elineSide', elineSide)
  .run(function(
    $log: ng.ILogService,
    $state: ng.ui.IStateService,
    XosNavigationService: any,
    XosComponentInjector: any) {
    $log.info('[metro-net-gui] App is running');

    XosNavigationService.add({
      label: 'Metronet GUI',
      state: 'xos.metro-net-gui',
    });

  });
