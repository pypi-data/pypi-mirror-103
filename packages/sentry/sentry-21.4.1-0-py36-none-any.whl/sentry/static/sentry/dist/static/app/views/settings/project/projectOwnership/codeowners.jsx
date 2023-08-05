import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import RulesPanel from 'app/views/settings/project/projectOwnership/rulesPanel';
var CodeOwnersPanel = /** @class */ (function (_super) {
    __extends(CodeOwnersPanel, _super);
    function CodeOwnersPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (codeowner) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, endpoint, codeowners, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, project = _a.project;
                        endpoint = "/api/0/projects/" + organization.slug + "/" + project.slug + "/codeowners/" + codeowner.id + "/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _c.sent();
                        codeowners = this.state.codeowners;
                        this.setState({
                            codeowners: codeowners.filter(function (config) { return config.id !== codeowner.id; }),
                        });
                        addSuccessMessage(t('Deletion successful'));
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        //no 4xx errors should happen on delete
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    CodeOwnersPanel.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [
            [
                'codeowners',
                "/projects/" + organization.slug + "/" + project.slug + "/codeowners/?expand=codeMapping",
            ],
        ];
    };
    CodeOwnersPanel.prototype.renderBody = function () {
        var _this = this;
        var codeowners = this.state.codeowners;
        return codeowners.map(function (codeowner) {
            var raw = codeowner.raw, dateUpdated = codeowner.dateUpdated, provider = codeowner.provider, repoName = codeowner.codeMapping.repoName;
            return (<React.Fragment key={codeowner.id}>
          <RulesPanel data-test-id="codeowners-panel" type="codeowners" raw={raw} dateUpdated={dateUpdated} provider={provider} repoName={repoName} readOnly controls={[
                    <Confirm onConfirm={function () { return _this.handleDelete(codeowner); }} message={t('Are you sure you want to remove this CODEOWNERS file?')} key="confirm-delete">
                <Button key="delete" icon={<IconDelete size="xs"/>} size="xsmall"/>
              </Confirm>,
                ]}/>
        </React.Fragment>);
        });
    };
    return CodeOwnersPanel;
}(AsyncComponent));
export default CodeOwnersPanel;
//# sourceMappingURL=codeowners.jsx.map