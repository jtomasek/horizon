var horizonApp = angular.module('horizonApp', ['ui.bootstrap']);

var ModalInstanceCtrl = function ($scope, $modalInstance, items) {

    $scope.allGroups = items;
    $scope.domainGroups = [];

    $scope.selected = {
        item: $scope.items[0]
    };

    $scope.ok = function () {
        $modalInstance.close($scope.selected.item);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.addToDomain = function (group) {
        $scope.domainGroups.push(group);
        var index = $scope.allGroups.indexOf(group);
        $scope.allGroups.splice(index, 1);
    };

    $scope.removeFromDomain = function (group) {
        var index = $scope.domainGroups.indexOf(group);
        $scope.domainGroups.splice(index, 1);
        $scope.allGroups.push(group);
    };

};


angular.module('horizonApp').controller('DomainGroupController',
  ['$scope', '$modal',
  function($scope, $modal) {

    $scope.allGroups = [
        'Group One',
        'Heres a Group'
    ];

    $scope.open = function () {

        var modalInstance = $modal.open({
            templateUrl: 'group_modal.html',
            controller: ModalInstanceCtrl,
            resolve: {
                items: function () {
                    return $scope.allGroups;
                }
            }
        })

    };
}]);

horizonApp.filter('searchFor', function () {
    return function (arr, searchString) {
        if (!searchString) {
            return arr;
        }
        var result = [];
        angular.forEach(arr, function (item) {
            if (item.toLowerCase().indexOf(searchString.toLowerCase()) !== -1) {
                result.push(item);
            }
        });
        return result;
    };


});