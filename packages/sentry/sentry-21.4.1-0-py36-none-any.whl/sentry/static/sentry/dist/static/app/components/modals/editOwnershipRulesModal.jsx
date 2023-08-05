import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import OwnershipModal from 'app/views/settings/project/projectOwnership/editRulesModal';
var EditOwnershipRulesModal = function (_a) {
    var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal, onSave = _a.onSave, props = __rest(_a, ["Body", "Header", "closeModal", "onSave"]);
    return (<React.Fragment>
      <Header closeButton onHide={closeModal}>
        {t('Edit Ownership Rules')}
      </Header>
      <Body>
        <OwnershipModal {...props} onSave={onSave}/>
      </Body>
    </React.Fragment>);
};
export var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 80%;\n      margin-left: -40%;\n    }\n  }\n  .modal-content {\n    overflow: initial;\n  }\n\n  .modal-header {\n    font-size: 20px;\n    font-weight: bold;\n  }\n"], ["\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 80%;\n      margin-left: -40%;\n    }\n  }\n  .modal-content {\n    overflow: initial;\n  }\n\n  .modal-header {\n    font-size: 20px;\n    font-weight: bold;\n  }\n"])), theme.breakpoints[0]);
export default EditOwnershipRulesModal;
var templateObject_1;
//# sourceMappingURL=editOwnershipRulesModal.jsx.map