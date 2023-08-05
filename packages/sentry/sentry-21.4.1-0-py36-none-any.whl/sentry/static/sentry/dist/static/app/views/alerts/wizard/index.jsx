import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import CreateAlertButton from 'app/components/createAlertButton';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import space from 'app/styles/space';
import BuilderBreadCrumbs from 'app/views/alerts/builder/builderBreadCrumbs';
import { Dataset } from 'app/views/settings/incidentRules/types';
import { AlertWizardAlertNames, AlertWizardOptions, AlertWizardPanelContent, AlertWizardRuleTemplates, } from './options';
import RadioPanelGroup from './radioPanelGroup';
var AlertWizard = /** @class */ (function (_super) {
    __extends(AlertWizard, _super);
    function AlertWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertOption: null,
        };
        _this.handleChangeAlertOption = function (alertOption) {
            _this.setState({ alertOption: alertOption });
        };
        return _this;
    }
    AlertWizard.prototype.renderCreateAlertButton = function () {
        var _a;
        var _b = this.props, organization = _b.organization, project = _b.project, location = _b.location;
        var alertOption = this.state.alertOption;
        var metricRuleTemplate = alertOption && AlertWizardRuleTemplates[alertOption];
        var disabled = !organization.features.includes('performance-view') &&
            (metricRuleTemplate === null || metricRuleTemplate === void 0 ? void 0 : metricRuleTemplate.dataset) === Dataset.TRANSACTIONS;
        var to = {
            pathname: "/organizations/" + organization.slug + "/alerts/" + project.slug + "/new/",
            query: __assign(__assign({}, (metricRuleTemplate && metricRuleTemplate)), { createFromWizard: true, referrer: (_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.referrer }),
        };
        return (<CreateAlertButton organization={organization} projectSlug={project.slug} priority="primary" to={to} disabled={disabled} hideIcon>
        {t('Set Conditions')}
      </CreateAlertButton>);
    };
    AlertWizard.prototype.render = function () {
        var _this = this;
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, organization = _a.organization, projectId = _a.params.projectId;
        var alertOption = this.state.alertOption;
        var title = t('Alert Creation Wizard');
        var panelContent = alertOption && AlertWizardPanelContent[alertOption];
        return (<React.Fragment>
        <SentryDocumentTitle title={title} projectSlug={projectId}/>

        <Feature features={['organizations:alert-wizard']}>
          <Layout.Header>
            <Layout.HeaderContent>
              <BuilderBreadCrumbs hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} projectSlug={projectId} title={t('Create Alert Rule')}/>
              <Layout.Title>{t('What should we alert you about?')}</Layout.Title>
            </Layout.HeaderContent>
          </Layout.Header>
          <StyledLayoutBody>
            <Layout.Main fullWidth>
              <WizardBody>
                <WizardOptions>
                  <Styledh2>{t('Errors')}</Styledh2>
                  {AlertWizardOptions.map(function (_a, i) {
                var categoryHeading = _a.categoryHeading, options = _a.options;
                return (<OptionsWrapper key={categoryHeading}>
                      {i > 0 && <Styledh2>{categoryHeading}</Styledh2>}
                      <RadioPanelGroup choices={options.map(function (alertType) {
                        return [alertType, AlertWizardAlertNames[alertType]];
                    })} onChange={_this.handleChangeAlertOption} value={alertOption} label="alert-option"/>
                    </OptionsWrapper>);
            })}
                </WizardOptions>
                <WizardPanel visible={!!panelContent && !!alertOption}>
                  <WizardPanelBody>
                    {panelContent && alertOption && (<div>
                        <PanelHeader>{AlertWizardAlertNames[alertOption]}</PanelHeader>
                        <PanelBody withPadding>
                          <PanelDescription>
                            {panelContent.description}{' '}
                            {panelContent.docsLink && (<ExternalLink href={panelContent.docsLink}>
                                {t('Learn more')}
                              </ExternalLink>)}
                          </PanelDescription>
                          <WizardImage src={panelContent.illustration}/>
                          <ExampleHeader>{t('Examples')}</ExampleHeader>
                          <ExampleList symbol="bullet">
                            {panelContent.examples.map(function (example, i) { return (<ExampleItem key={i}>{example}</ExampleItem>); })}
                          </ExampleList>
                        </PanelBody>
                      </div>)}
                    <WizardButton>{this.renderCreateAlertButton()}</WizardButton>
                  </WizardPanelBody>
                </WizardPanel>
              </WizardBody>
            </Layout.Main>
          </StyledLayoutBody>
        </Feature>
      </React.Fragment>);
    };
    return AlertWizard;
}(React.Component));
var StyledLayoutBody = styled(Layout.Body)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: -", ";\n"], ["\n  margin-bottom: -", ";\n"])), space(3));
var Styledh2 = styled('h2')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: normal;\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"], ["\n  font-weight: normal;\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"])), function (p) { return p.theme.fontSizeLarge; }, space(1));
var WizardBody = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  padding-top: ", ";\n"], ["\n  display: flex;\n  padding-top: ", ";\n"])), space(1));
var WizardOptions = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 3;\n  margin-right: ", ";\n  padding-right: ", ";\n  max-width: 300px;\n"], ["\n  flex: 3;\n  margin-right: ", ";\n  padding-right: ", ";\n  max-width: 300px;\n"])), space(3), space(3));
var WizardImage = styled('img')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  max-height: 300px;\n"], ["\n  max-height: 300px;\n"])));
var WizardPanel = styled(Panel)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  max-width: 700px;\n  position: sticky;\n  top: 20px;\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n  ", ";\n\n  @keyframes pop {\n    0% {\n      transform: translateY(30px);\n      opacity: 0;\n    }\n    100% {\n      transform: translateY(0);\n      opacity: 1;\n    }\n  }\n"], ["\n  max-width: 700px;\n  position: sticky;\n  top: 20px;\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n  ", ";\n\n  @keyframes pop {\n    0% {\n      transform: translateY(30px);\n      opacity: 0;\n    }\n    100% {\n      transform: translateY(0);\n      opacity: 1;\n    }\n  }\n"])), function (p) { return !p.visible && 'visibility: hidden'; }, function (p) { return p.visible && 'animation: 0.6s pop ease forwards'; });
var ExampleList = styled(List)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-bottom: ", " !important;\n"], ["\n  margin-bottom: ", " !important;\n"])), space(2));
var WizardPanelBody = styled(PanelBody)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex: 1;\n  min-width: 100%;\n"], ["\n  flex: 1;\n  min-width: 100%;\n"])));
var PanelDescription = styled('p')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var ExampleHeader = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  margin: 0 0 ", " 0;\n  font-size: ", ";\n"], ["\n  margin: 0 0 ", " 0;\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeLarge; });
var ExampleItem = styled(ListItem)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var OptionsWrapper = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"], ["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"])), space(4));
var WizardButton = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: ", " ", " ", " ", ";\n"], ["\n  border-top: 1px solid ", ";\n  padding: ", " ", " ", " ", ";\n"])), function (p) { return p.theme.border; }, space(1.5), space(1.5), space(1.5), space(1.5));
export default AlertWizard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=index.jsx.map