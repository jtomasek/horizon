var myApp = angular.module('myApp', []);

function MyCtrl($scope) {
    $scope.name = { name: 'Superhero' };
    $scope.allGroups = [
        'Group One',
        'Heres a Group', ];

    $scope.domainGroups = [];
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
}

myApp.filter('searchFor', function () {
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