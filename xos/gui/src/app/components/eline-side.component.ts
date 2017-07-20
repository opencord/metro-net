let self;

class ElineSide {

  static $inject = ['XosSidePanel', 'XosModelStore', '$http', '$log', 'toastr'];

  constructor(
    private XosSidePanel: any,
    private XosModelStore: any,
    private $http: any,
    private $log: any,
    private toastr: any,
  ) {
    self = this;
  }

  public saveEline(item: any) {
    let path = item.path;
    delete item.path;
    item.$save().then((res) => {
      item.path = path;
      this.toastr.success(`${item.name} successfully saved!`);
    })
      .catch((error) => {
        this.toastr.error(`Error while saving ${item.name}: ${error.specific_error}`);
      });
  }


}

export const elineSide: angular.IComponentOptions = {
  template: require('./eline-side.component.html'),
  controllerAs: 'vm',
  controller: ElineSide,
  bindings: {
    mng: '='
  }
};
