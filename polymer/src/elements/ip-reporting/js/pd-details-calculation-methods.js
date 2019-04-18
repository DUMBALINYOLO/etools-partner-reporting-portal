function PdDetailsCalculationMethodsUtils() {

};

PdDetailsCalculationMethodsUtils.computeIndicatorsUrl = function(locationId, pdId) {
    return locationId ? App.Endpoints.calculationMethods(locationId, pdId) : '';
};

PdDetailsCalculationMethodsUtils.computeFormattedData = function(data) {
    return data.ll_outputs_and_indicators.reduce(function (acc, curr) {
        var items;

        acc.push({
            type: 'label',
            text: curr.ll_output.title,
        });

        items = curr.indicators.map(function (indicator) {
            return {
                type: 'data',
                data: Object.assign({}, indicator, {
                    editable: true,
                }),
                llo_id: curr.ll_output.id,
            };
        });

        acc.push.apply(acc, items);

        return acc;
    }, []);
};

PdDetailsCalculationMethodsUtils.computeSelected = function(data, scope) {
    return data[scope];
};

PdDetailsCalculationMethodsUtils.computeDisabled = function(display_type) {
    return ['percentage', 'ratio'].indexOf(display_type) !== -1;
};

try {
    module.exports = exports = PdDetailsCalculationMethodsUtils;
} catch (e) {}
