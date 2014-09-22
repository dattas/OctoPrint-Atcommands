$(function() {
    function AtCommandsViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];
        self.settingsViewModel = parameters[1];

        self.chooseInstance = function(data) {
            self.settings.plugins.atcommands.at_pause_commands(data.at_pause_commands);
        };

        self.fromResponse = function(response) {
        };

        self.requestData = function () {
            $.ajax({
                url: API_BASEURL + "plugin/atcommands",
                type: "GET",
                dataType: "json",
                success: self.fromResponse
            });
        };

        self.onBeforeBinding = function() {
            self.settings = self.settingsViewModel.settings;
            /*self.requestData();*/
        };

        self.onSettingsShown = function() {
            /*self.requestData();*/
        };
    }

    ADDITIONAL_VIEWMODELS.push([AtCommandsViewModel, ["loginStateViewModel", "settingsViewModel"], document.getElementById("settings_plugin_atcommands_dialog")]);
});