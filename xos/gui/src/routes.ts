export default routesConfig;

function routesConfig($stateProvider: angular.ui.IStateProvider, $locationProvider: angular.ILocationProvider) {
  $locationProvider.html5Mode(false).hashPrefix('');

  $stateProvider
    .state('xos.metro-net-gui', {
      url: 'metro-net-gui',
      parent: 'xos',
      component: 'mngMap'
    });
}
