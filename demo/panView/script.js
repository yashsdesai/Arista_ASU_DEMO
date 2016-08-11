function FetchCtrl($scope, $http, $templateCache) {
    // Use this for jsonp
    // http://localhost:8080/something?callback=JSON_CALLBACK&name=Super%20Hero
    $scope.method = 'POST';
    $scope.url = 'http://localhost:8080/something';
// This doesn't seem like its going to work without modifiction on the server (switch) side
    $scope.fetch = function() {
        $scope.code = null;
        $scope.response = null;
//        $scope.datarequest = {"jsonrpc":"2.0", "method": "runCmds", "params": { "version": 1,
//            "cmds":["show version"], "format": "json"}, "id":1}
        $http.jsonp($scope.url, 
                {method: $scope.method, 
                    cache: $templateCache,
                    headers: {'Content-Type': 'application/json'},
                    data: $scope.datarequest}).
            success(function(data, status) {
                $scope.status = status;
                $scope.data = data;
                $scope.switches = data.switches
            }).
        error(function(data, status) {
            $scope.data = data || "Request failed";
            $scope.status = status;
        });
    };

    $scope.updateModel = function(method, url) {
        $scope.method = method;
        $scope.url = url;
    };
}
