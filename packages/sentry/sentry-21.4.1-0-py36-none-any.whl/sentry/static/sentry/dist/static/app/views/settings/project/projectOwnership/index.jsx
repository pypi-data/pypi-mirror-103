import { __assign, __extends } from "tslib";
import React from 'react';
import { openEditOwnershipRules } from 'app/actionCreators/modal';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import CodeOwnersPanel from 'app/views/settings/project/projectOwnership/codeowners';
import RulesPanel from 'app/views/settings/project/projectOwnership/rulesPanel';
var ProjectOwnership = /** @class */ (function (_super) {
    __extends(ProjectOwnership, _super);
    function ProjectOwnership() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleOwnershipSave = function (text) {
            _this.setState(function (prevState) { return ({
                ownership: __assign(__assign({}, prevState.ownership), { raw: text }),
            }); });
        };
        return _this;
    }
    ProjectOwnership.prototype.getTitle = function () {
        var project = this.props.project;
        return routeTitleGen(t('Issue Owners'), project.slug, false);
    };
    ProjectOwnership.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [['ownership', "/projects/" + organization.slug + "/" + project.slug + "/ownership/"]];
    };
    ProjectOwnership.prototype.getPlaceholder = function () {
        return "#example usage\npath:src/example/pipeline/* person@sentry.io #infra\nurl:http://example.com/settings/* #product\ntags.sku_class:enterprise #enterprise";
    };
    ProjectOwnership.prototype.getDetail = function () {
        return tct("Automatically assign issues and send alerts to the right people based on issue properties. [link:Learn more].", {
            link: (<ExternalLink href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
        });
    };
    ProjectOwnership.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, project = _a.project, organization = _a.organization;
        var ownership = this.state.ownership;
        var disabled = !organization.access.includes('project:write');
        return (<React.Fragment>
        <SettingsPageHeader title={t('Issue Owners')} action={<Button to={{
                    pathname: "/organizations/" + organization.slug + "/issues/",
                    query: { project: project.id },
                }} size="small">
              {t('View Issues')}
            </Button>}/>
        <PermissionAlert />
        <RulesPanel data-test-id="issueowners-panel" type="issueowners" raw={ownership.raw || ''} dateUpdated={ownership.lastUpdated} placeholder={this.getPlaceholder()} detail={this.getDetail()} controls={[
                <Button key="edit" size="small" onClick={function () {
                        return openEditOwnershipRules({
                            organization: organization,
                            project: project,
                            ownership: ownership,
                            onSave: _this.handleOwnershipSave,
                        });
                    }} disabled={disabled}>
              {t('Edit')}
            </Button>,
            ]}/>
        <Feature features={['import-codeowners']}>
          <CodeOwnersPanel {...this.props}/>
        </Feature>
        <Form apiEndpoint={"/projects/" + organization.slug + "/" + project.slug + "/ownership/"} apiMethod="PUT" saveOnBlur initialData={{ fallthrough: ownership.fallthrough }} hideFooter>
          <JsonForm forms={[
                {
                    title: t('If ownership cannot be determined for an issue...'),
                    fields: [
                        {
                            name: 'fallthrough',
                            type: 'boolean',
                            label: t('All users with access to this project are issue owners'),
                            help: t('Issue owners will receive notifications for issues they are responsible for.'),
                            disabled: disabled,
                        },
                    ],
                },
            ]}/>
        </Form>

        <Form apiEndpoint={"/projects/" + organization.slug + "/" + project.slug + "/ownership/"} apiMethod="PUT" saveOnBlur initialData={{ autoAssignment: ownership.autoAssignment }} hideFooter>
          <JsonForm forms={[
                {
                    title: t('If a new event matches any of the ownership rules...'),
                    fields: [
                        {
                            name: 'autoAssignment',
                            type: 'boolean',
                            label: t('The issue is assigned to the team or user'),
                            help: t('Issue owners will be automatically assigned.'),
                            disabled: disabled,
                        },
                    ],
                },
            ]}/>
        </Form>
      </React.Fragment>);
    };
    return ProjectOwnership;
}(AsyncView));
export default ProjectOwnership;
//# sourceMappingURL=index.jsx.map