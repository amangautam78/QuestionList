/*global gettext, interpolate, ngettext*/
'use strict';
{
<<<<<<< HEAD
    function show(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.remove('hidden');
        });
    }

    function hide(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.add('hidden');
        });
    }

    function showQuestion(options) {
        hide(options.acrossClears);
        show(options.acrossQuestions);
        hide(options.allContainer);
    }

    function showClear(options) {
        show(options.acrossClears);
        hide(options.acrossQuestions);
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
        show(options.allContainer);
        hide(options.counterContainer);
    }

    function reset(options) {
        hide(options.acrossClears);
        hide(options.acrossQuestions);
        hide(options.allContainer);
        show(options.counterContainer);
    }

    function clearAcross(options) {
        reset(options);
        const acrossInputs = document.querySelectorAll(options.acrossInput);
        acrossInputs.forEach(function(acrossInput) {
            acrossInput.value = 0;
        });
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
    }

    function checker(actionCheckboxes, options, checked) {
        if (checked) {
            showQuestion(options);
        } else {
            reset(options);
        }
        actionCheckboxes.forEach(function(el) {
            el.checked = checked;
            el.closest('tr').classList.toggle(options.selectedClass, checked);
        });
    }

    function updateCounter(actionCheckboxes, options) {
        const sel = Array.from(actionCheckboxes).filter(function(el) {
            return el.checked;
        }).length;
        const counter = document.querySelector(options.counterContainer);
        // data-actions-icnt is defined in the generated HTML
        // and contains the total amount of objects in the queryset
        const actions_icnt = Number(counter.dataset.actionsIcnt);
        counter.textContent = interpolate(
            ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
                sel: sel,
                cnt: actions_icnt
            }, true);
        const allToggle = document.getElementById(options.allToggleId);
        allToggle.checked = sel === actionCheckboxes.length;
        if (allToggle.checked) {
            showQuestion(options);
        } else {
            clearAcross(options);
        }
    }

    const defaults = {
=======
    const $ = django.jQuery;
    let lastChecked;

    $.fn.actions = function(opts) {
        const options = $.extend({}, $.fn.actions.defaults, opts);
        const actionCheckboxes = $(this);
        let list_editable_changed = false;
        const showQuestion = function() {
                $(options.acrossClears).hide();
                $(options.acrossQuestions).show();
                $(options.allContainer).hide();
            },
            showClear = function() {
                $(options.acrossClears).show();
                $(options.acrossQuestions).hide();
                $(options.actionContainer).toggleClass(options.selectedClass);
                $(options.allContainer).show();
                $(options.counterContainer).hide();
            },
            reset = function() {
                $(options.acrossClears).hide();
                $(options.acrossQuestions).hide();
                $(options.allContainer).hide();
                $(options.counterContainer).show();
            },
            clearAcross = function() {
                reset();
                $(options.acrossInput).val(0);
                $(options.actionContainer).removeClass(options.selectedClass);
            },
            checker = function(checked) {
                if (checked) {
                    showQuestion();
                } else {
                    reset();
                }
                $(actionCheckboxes).prop("checked", checked)
                    .parent().parent().toggleClass(options.selectedClass, checked);
            },
            updateCounter = function() {
                const sel = $(actionCheckboxes).filter(":checked").length;
                // data-actions-icnt is defined in the generated HTML
                // and contains the total amount of objects in the queryset
                const actions_icnt = $('.action-counter').data('actionsIcnt');
                $(options.counterContainer).html(interpolate(
                    ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
                        sel: sel,
                        cnt: actions_icnt
                    }, true));
                $(options.allToggle).prop("checked", function() {
                    let value;
                    if (sel === actionCheckboxes.length) {
                        value = true;
                        showQuestion();
                    } else {
                        value = false;
                        clearAcross();
                    }
                    return value;
                });
            };
        // Show counter by default
        $(options.counterContainer).show();
        // Check state of checkboxes and reinit state if needed
        $(this).filter(":checked").each(function(i) {
            $(this).parent().parent().toggleClass(options.selectedClass);
            updateCounter();
            if ($(options.acrossInput).val() === 1) {
                showClear();
            }
        });
        $(options.allToggle).show().on('click', function() {
            checker($(this).prop("checked"));
            updateCounter();
        });
        $("a", options.acrossQuestions).on('click', function(event) {
            event.preventDefault();
            $(options.acrossInput).val(1);
            showClear();
        });
        $("a", options.acrossClears).on('click', function(event) {
            event.preventDefault();
            $(options.allToggle).prop("checked", false);
            clearAcross();
            checker(0);
            updateCounter();
        });
        lastChecked = null;
        $(actionCheckboxes).on('click', function(event) {
            if (!event) { event = window.event; }
            const target = event.target ? event.target : event.srcElement;
            if (lastChecked && $.data(lastChecked) !== $.data(target) && event.shiftKey === true) {
                let inrange = false;
                $(lastChecked).prop("checked", target.checked)
                    .parent().parent().toggleClass(options.selectedClass, target.checked);
                $(actionCheckboxes).each(function() {
                    if ($.data(this) === $.data(lastChecked) || $.data(this) === $.data(target)) {
                        inrange = (inrange) ? false : true;
                    }
                    if (inrange) {
                        $(this).prop("checked", target.checked)
                            .parent().parent().toggleClass(options.selectedClass, target.checked);
                    }
                });
            }
            $(target).parent().parent().toggleClass(options.selectedClass, target.checked);
            lastChecked = target;
            updateCounter();
        });
        $('form#changelist-form table#result_list tr').on('change', 'td:gt(0) :input', function() {
            list_editable_changed = true;
        });
        $('form#changelist-form button[name="index"]').on('click', function(event) {
            if (list_editable_changed) {
                return confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));
            }
        });
        $('form#changelist-form input[name="_save"]').on('click', function(event) {
            let action_changed = false;
            $('select option:selected', options.actionContainer).each(function() {
                if ($(this).val()) {
                    action_changed = true;
                }
            });
            if (action_changed) {
                if (list_editable_changed) {
                    return confirm(gettext("You have selected an action, but you haven’t saved your changes to individual fields yet. Please click OK to save. You’ll need to re-run the action."));
                } else {
                    return confirm(gettext("You have selected an action, and you haven’t made any changes on individual fields. You’re probably looking for the Go button rather than the Save button."));
                }
            }
        });
    };
    /* Setup plugin defaults */
    $.fn.actions.defaults = {
>>>>>>> 3b568933b8ffaa9fd7f40506bf945986e5a961ea
        actionContainer: "div.actions",
        counterContainer: "span.action-counter",
        allContainer: "div.actions span.all",
        acrossInput: "div.actions input.select-across",
        acrossQuestions: "div.actions span.question",
        acrossClears: "div.actions span.clear",
<<<<<<< HEAD
        allToggleId: "action-toggle",
        selectedClass: "selected"
    };

    window.Actions = function(actionCheckboxes, options) {
        options = Object.assign({}, defaults, options);
        let list_editable_changed = false;
        let lastChecked = null;
        let shiftPressed = false;

        document.addEventListener('keydown', (event) => {
            shiftPressed = event.shiftKey;
        });

        document.addEventListener('keyup', (event) => {
            shiftPressed = event.shiftKey;
        });

        document.getElementById(options.allToggleId).addEventListener('click', function(event) {
            checker(actionCheckboxes, options, this.checked);
            updateCounter(actionCheckboxes, options);
        });

        document.querySelectorAll(options.acrossQuestions + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                const acrossInputs = document.querySelectorAll(options.acrossInput);
                acrossInputs.forEach(function(acrossInput) {
                    acrossInput.value = 1;
                });
                showClear(options);
            });
        });

        document.querySelectorAll(options.acrossClears + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                document.getElementById(options.allToggleId).checked = false;
                clearAcross(options);
                checker(actionCheckboxes, options, false);
                updateCounter(actionCheckboxes, options);
            });
        });

        function affectedCheckboxes(target, withModifier) {
            const multiSelect = (lastChecked && withModifier && lastChecked !== target);
            if (!multiSelect) {
                return [target];
            }
            const checkboxes = Array.from(actionCheckboxes);
            const targetIndex = checkboxes.findIndex(el => el === target);
            const lastCheckedIndex = checkboxes.findIndex(el => el === lastChecked);
            const startIndex = Math.min(targetIndex, lastCheckedIndex);
            const endIndex = Math.max(targetIndex, lastCheckedIndex);
            const filtered = checkboxes.filter((el, index) => (startIndex <= index) && (index <= endIndex));
            return filtered;
        };

        Array.from(document.getElementById('result_list').tBodies).forEach(function(el) {
            el.addEventListener('change', function(event) {
                const target = event.target;
                if (target.classList.contains('action-select')) {
                    const checkboxes = affectedCheckboxes(target, shiftPressed);
                    checker(checkboxes, options, target.checked);
                    updateCounter(actionCheckboxes, options);
                    lastChecked = target;
                } else {
                    list_editable_changed = true;
                }
            });
        });

        document.querySelector('#changelist-form button[name=index]').addEventListener('click', function(event) {
            if (list_editable_changed) {
                const confirmed = confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));
                if (!confirmed) {
                    event.preventDefault();
                }
            }
        });

        const el = document.querySelector('#changelist-form input[name=_save]');
        // The button does not exist if no fields are editable.
        if (el) {
            el.addEventListener('click', function(event) {
                if (document.querySelector('[name=action]').value) {
                    const text = list_editable_changed
                        ? gettext("You have selected an action, but you haven’t saved your changes to individual fields yet. Please click OK to save. You’ll need to re-run the action.")
                        : gettext("You have selected an action, and you haven’t made any changes on individual fields. You’re probably looking for the Go button rather than the Save button.");
                    if (!confirm(text)) {
                        event.preventDefault();
                    }
                }
            });
        }
        // Sync counter when navigating to the page, such as through the back
        // button.
        window.addEventListener('pageshow', (event) => updateCounter(actionCheckboxes, options));
    };

    // Call function fn when the DOM is loaded and ready. If it is already
    // loaded, call the function now.
    // http://youmightnotneedjquery.com/#ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(function() {
        const actionsEls = document.querySelectorAll('tr input.action-select');
        if (actionsEls.length > 0) {
            Actions(actionsEls);
=======
        allToggle: "#action-toggle",
        selectedClass: "selected"
    };
    $(document).ready(function() {
        const $actionsEls = $('tr input.action-select');
        if ($actionsEls.length > 0) {
            $actionsEls.actions();
>>>>>>> 3b568933b8ffaa9fd7f40506bf945986e5a961ea
        }
    });
}
