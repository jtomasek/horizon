angular.module('horizonApp').directive('hrMembership',
    function() {
        return {
            restrict: 'A',
            replace: true,
            scope: { step: '=',
                     stepSlug: '=',
                     stepShowRoles: '=',
                     stepHelpText: '=',
                     stepAvailableListTitle: '=',
                     stepMembersListTitle: '=',
                     stepNoAvailableText: '=',
                     stepNoMembersText: '=',
                     jsonDataUrl: '=' },
            templateUrl: 'membership_workflow.html',
            controller: 'MembershipController',
            link: function(scope, element, attrs) {}
        };
    })
.factory('MembershipFactory', ['$http', function($http) {
    return {
        getData: function(url, success_callback) {
            $http.get(url)
                .success(success_callback)
                .error(function(data, status) {
                    console.log(status);
                    console.log(data);
                }
            );
        }
    };
}])
.controller('MembershipController',
    ['$scope', '$filter', '$http', 'horizon', 'MembershipFactory',
    function($scope, $filter, $http, horizon, MembershipFactory) {
        MembershipFactory.getData($scope.jsonDataUrl, function(data, status) {
           $scope.role_structure = data;
        });

        // Watch the roles model for changes and regenerate members
        $scope.$watchCollection('role_structure.roles', function(updatedRoles) {
            if( ! updatedRoles ) { return; }
            angular.forEach(updatedRoles, function(role, index) {
                $scope.$watchCollection('role_structure.roles['+index+'].selected_groups', function(updatedSelectedGroups, oldSelectedGroups) {
                    if( ! updatedSelectedGroups ) { return; }
                    $scope.regenerateMembers();
                });
            });
        });

        $scope.regenerateMembers = function() {
            $scope.available = [];
            $scope.members = [];
            angular.forEach($scope.role_structure.groups, function(group) {
                if($scope.rolesForGroup(group).length > 0) {
                    $scope.members.push(group);
                } else {
                    $scope.available.push(group);
                }
            });
        };

        $scope.rolesForGroup = function(group) {
            return $filter('filter')($scope.role_structure.roles, function(role) {
                return role.selected_groups.indexOf(group.id) > -1;
            });
        };

        $scope.groupHasRole = function(group, role) {
            return $scope.rolesForGroup(group).indexOf(role) > -1;
        };

        $scope.roleHasGroupSelected = function(role, group_id) {
            return role.selected_groups.indexOf(group_id) > -1;
        };

        $scope.rolesText = function(group) {
            var names = [];
            angular.forEach($scope.rolesForGroup(group), function(role) {
                names.push(role.name);
            });
            return names.slice(0,2).join(', ') + (names.length > 2 ? ",..." : "");
        };

        $scope.toggleRole = function(group_id, role) {
            if(role.selected_groups.indexOf(group_id) > -1) {
                var index = role.selected_groups.indexOf(group_id);
                role.selected_groups.splice(index, 1);
            } else {
                role.selected_groups.push(group_id);
            }
        };

        $scope.addMember = function(group){
            var default_role = $filter('filter')($scope.role_structure.roles, { id: $scope.role_structure.default_role_id })[0];
            default_role.selected_groups.push(group.id);
        };

        $scope.removeMember = function(group) {
            angular.forEach($scope.rolesForGroup(group), function(role) {
                var index = role.selected_groups.indexOf(group.id);
                role.selected_groups.splice(index, 1);
            });
        };

    }]);
