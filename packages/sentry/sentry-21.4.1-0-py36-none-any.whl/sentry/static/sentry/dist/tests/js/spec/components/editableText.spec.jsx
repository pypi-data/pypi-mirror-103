import React from 'react';
import { act } from 'react-dom/test-utils';
import { createListeners } from 'sentry-test/createListeners';
import { mountWithTheme } from 'sentry-test/enzyme';
import EditableText from 'app/components/editableText';
function renderedComponent(onChange, newValue) {
    if (newValue === void 0) { newValue = 'bar'; }
    var currentValue = 'foo';
    var wrapper = mountWithTheme(<EditableText value={currentValue} onChange={onChange}/>);
    var content = wrapper.find('Content');
    expect(content.text()).toEqual(currentValue);
    var inputWrapper = wrapper.find('InputWrapper');
    expect(inputWrapper.length).toEqual(0);
    var styledIconEdit = wrapper.find('StyledIconEdit');
    expect(styledIconEdit).toBeTruthy();
    content.simulate('click');
    content = wrapper.find('Content');
    expect(inputWrapper.length).toEqual(0);
    inputWrapper = wrapper.find('InputWrapper');
    expect(inputWrapper).toBeTruthy();
    var styledInput = wrapper.find('StyledInput');
    expect(styledInput).toBeTruthy();
    styledInput.simulate('change', { target: { value: newValue } });
    var inputLabel = wrapper.find('InputLabel');
    expect(inputLabel.text()).toEqual(newValue);
    return wrapper;
}
describe('EditableText', function () {
    var currentValue = 'foo';
    var newValue = 'bar';
    it('edit value and click outside of the component', function () {
        var fireEvent = createListeners('document');
        var handleChange = jest.fn();
        var wrapper = renderedComponent(handleChange);
        act(function () {
            // Click outside of the component
            fireEvent.mouseDown(document.body);
        });
        expect(handleChange).toHaveBeenCalled();
        wrapper.update();
        var updatedContent = wrapper.find('Content');
        expect(updatedContent).toBeTruthy();
        expect(updatedContent.text()).toEqual(newValue);
    });
    it('edit value and press enter', function () {
        var fireEvent = createListeners('window');
        var handleChange = jest.fn();
        var wrapper = renderedComponent(handleChange);
        act(function () {
            // Press enter
            fireEvent.keyDown('Enter');
        });
        expect(handleChange).toHaveBeenCalled();
        wrapper.update();
        var updatedContent = wrapper.find('Content');
        expect(updatedContent).toBeTruthy();
        expect(updatedContent.text()).toEqual(newValue);
    });
    it('edit value and press escape', function () {
        var fireEvent = createListeners('window');
        var handleChange = jest.fn();
        var wrapper = renderedComponent(handleChange);
        act(function () {
            // Press escape
            fireEvent.keyDown('Escape');
        });
        expect(handleChange).toHaveBeenCalledTimes(0);
        wrapper.update();
        var updatedContent = wrapper.find('Content');
        expect(updatedContent).toBeTruthy();
        expect(updatedContent.text()).toEqual(currentValue);
    });
    it('clear value and show error message', function () {
        var fireEvent = createListeners('window');
        var handleChange = jest.fn();
        var wrapper = renderedComponent(handleChange, '');
        act(function () {
            // Press enter
            fireEvent.keyDown('Enter');
        });
        expect(handleChange).toHaveBeenCalledTimes(0);
        wrapper.update();
        var fieldControlErrorWrapper = wrapper.find('FieldControlErrorWrapper');
        expect(fieldControlErrorWrapper).toBeTruthy();
    });
});
//# sourceMappingURL=editableText.spec.jsx.map