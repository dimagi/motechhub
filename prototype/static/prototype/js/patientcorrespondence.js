hqDefine('prototype/js/patientcorrespondence.js', function () {
    function PatientCorrespondenceViewModel() {
        var self = {};
        self.expanded = ko.observable();
        self.patientIdentifierTypes = ko.observable();
        self.caseProperties = ko.observable();
        self.items = ko.observableArray();
        self.addItem = function (patientIdentifierType) {
            self.items.push({
                patientIdentifierType: patientIdentifierType,
                caseProperty: ko.observable()
            });
        };
        return self;

    }
    return {
        PatientCorrespondenceViewModel: PatientCorrespondenceViewModel
    };
});
