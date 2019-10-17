(function($) {



    var form = $("#signup-form");
    form.validate({
        errorPlacement: function errorPlacement(error, element) {
            element.before(error);
        },
        rules: {
            email: {
                email: true
            }
        },
        onfocusout: function(element) {
            $(element).valid();
        },
    });
    form.children("div").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        stepsOrientation: "vertical",
        titleTemplate: '<div class="title"><span class="step-number">#index#</span><span class="step-text">#title#</span></div>',
        labels: {
            current: "",
            pagination: "",
            finish: "Finalizar",
            next: "Siguiente",
            previous: "Retroceder",
            loading: ""

        },
        onStepChanging: function(event, currentIndex, newIndex) {
            if (currentIndex === 0) {
                if (checkSteps(0))
                {
                    _etmc.push(["setOrgId", "7321491"]);
                    _etmc.push(["setUserInfo", {"email":$("#email").val()}]);       
                    _etmc.push(["trackPageView"]);
                    form.parent().parent().parent().append('<div class="footer footer-' + currentIndex + '"></div>');
                }else{
                    return false;
                }
            }
            if (currentIndex === 1) {
                if (checkSteps(1))
                {
                    form.parent().parent().parent().append('<div class="footer footer-' + currentIndex + '"></div>');
                }else{
                    return false;
                }
            }
            if (currentIndex === 2) {
                if (checkSteps(2))
                {
                    form.parent().parent().parent().append('<div class="footer footer-' + currentIndex + '"></div>');
                }else{
                    return false;
                }
            }
            if (currentIndex === 3) {
                if (checkSteps(3))
                {
                    
                    form.parent().parent().parent().append('<div class="footer footer-' + currentIndex + '"></div>');

                }else{
                    return false;
                }
            }
            if(currentIndex === 4) {
                if (checkSteps(4))
                {
                    _etmc.push(["setOrgId", "7321491"]);
                    _etmc.push(["setUserInfo", {"email":$("#email").val()}]);       
                    _etmc.push(["setUserInfo", {"Value_1":"1"}]);
                    _etmc.push(["trackPageView"]);
                    form.parent().parent().parent().append('<div class="footer footer-' + currentIndex + '"></div>');
                }else{
                    return false;
                }
            }
            form.validate().settings.ignore = ":disabled,:hidden";
            return form.valid();
        },
        onFinishing: function(event, currentIndex) {
            form.validate().settings.ignore = ":disabled";
            return form.valid();
        },
        onFinished: function(event, currentIndex) {
            create_lead();
        },
        onStepChanged: function(event, currentIndex, priorIndex) {

            return true;
        }
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });

    $.dobPicker({
        daySelector: '#birth_date',
        monthSelector: '#birth_month',
        yearSelector: '#birth_year',
        dayDefault: '',
        monthDefault: '',
        yearDefault: '',
        minimumAge: 0,
        maximumAge: 80
    });
    var marginSlider = document.getElementById('slider-margin');
    if (marginSlider != undefined) {
        noUiSlider.create(marginSlider, {
              start: [1100],
              step: 100,
              connect: [true, false],
              tooltips: [true],
              range: {
                  'min': 100,
                  'max': 2000
              },
              pips: {
                    mode: 'values',
                    values: [100, 2000],
                    density: 4
                    },
                format: wNumb({
                    decimals: 0,
                    thousand: '',
                    prefix: '$ ',
                })
        });
        var marginMin = document.getElementById('value-lower'),
	    marginMax = document.getElementById('value-upper');

        marginSlider.noUiSlider.on('update', function ( values, handle ) {
            if ( handle ) {
                marginMax.innerHTML = values[handle];
            } else {
                marginMin.innerHTML = values[handle];
            }
        });
    }
})(jQuery);




