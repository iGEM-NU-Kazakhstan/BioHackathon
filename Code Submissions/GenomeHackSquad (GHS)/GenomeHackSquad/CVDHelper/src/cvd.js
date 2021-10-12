 (function(exports) {
  var curDelta = 0;
  var curSeverity = 0;
  var curType = 'PROTANOMALY';
  var curSimulate = false;
  var curEnable = false;
  var curFilter = 0;
  var cssContent = `html[cvd="0"]{-webkit-filter: url('#cvd_extension_0');}html[cvd="1"]{-webkit-filter: url('#cvd_extension_1');}`;

  /** @const {string} */
  var SVGDefaultMatrix = '1 0 0 0 0 ' + '0 1 0 0 0 ' + '0 0 1 0 0 ' + '0 0 0 1 0';

  var svgContent = `<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                      <defs>
                        <filter x="0" y="0" width="99999" height="99999" id="cvd_extension_0">
                          <feColorMatrix id="cvd_matrix_0" type="matrix" values="
                              ${SVGDefaultMatrix}"/>
                        </filter>
                        <filter x="0" y="0" width="99999" height="99999" id="cvd_extension_1">
                          <feColorMatrix id="cvd_matrix_1" type="matrix" values="
                              ${SVGDefaultMatrix}"/>
                        </filter>
                      </defs>
                    </svg>
                    `;

  /**
  @const {object}
   */
  var IdentityMatrix = [[1, 0, 0],[0, 1, 0],[0, 0, 1]];

  /**
  @param {!object} matrixA 
  @param {!object} matrixB 
  @return {!object} 
   */
  function matrixAddition(matrixA, matrixB) {
    var result = [];
    for (var i = 0; i < 3; i++) {
      result[i] = [];
      for (var j = 0; j < 3; j++) {
        result[i].push(matrixA[i][j] + matrixB[i][j]);
      }
    }
    return result;
  }

  /**
  @param {!object} matrixA 
  @param {!object} matrixB 
  @return {!object} 
   */
  function matrixSubtraction(matrixA, matrixB) {
    var result = [];
    for (var i = 0; i < 3; i++) {
      result[i] = [];
      for (var j = 0; j < 3; j++) {
        result[i].push(matrixA[i][j] - matrixB[i][j]);
      }
    }
    return result;
  }

  /**
  @param {!object} matrixA 
  @param {!object} matrixB 
  @return {!object}
   */
  function matrixMultiplication(matrixA, matrixB) {
    var result = [];
    for (var i = 0; i < 3; i++) {
      result[i] = [];
      for (var j = 0; j < 3; j++) {
        var TotalSum = 0;
        for (var k = 0; k < 3; k++) {
          TotalSum += matrixA[i][k] * matrixB[k][j];
        }
        result[i].push(TotalSum);
      }
    }
    return result;
  }

  /**
  @param {!object} matrixA
  @param {!number} N
  @return {!object}
   */
  function matrixScalarMultiplication(matrixA, N) {
    var result = [];
    for (var i = 0; i < 3; i++) {
      result[i] = [];
      for (var j = 0; j < 3; j++) {
        result[i].push(N * matrixA[i][j]);
      }
    }
    return result;
  }

  /**
  @param {!object} matrixA 
  @return {!string}
   */
  function SVGMatrixString(matrixA) {
    var outputRows = [];
    for (var i = 0; i < 3; i++) {
      outputRows.push(matrixA[i].join(' ') + ' 0 0');
    }
    outputRows.push('0 0 0 1 0');
    return outputRows.join(' ');
  }

  /**
  @param {!object} matrixA
  @return {!string} 
   */
  function NewMatrixString(matrixA) {
      var result = '';
      for (var i = 0; i < 3; i++) {
          result += (i ? ', ' : '') + '[';
          for (var j = 0; j < 3; j++) {
              result += (j ? ', ' : '') + matrixA[i][j].toFixed(2);
          }
          result += ']';
      }
      return result;
  }



  /**
  @enum {string}
   */
  var cvdSimulationParams = { PROTANOMALY: [[0.4720, -1.2946, 0.9857],
                                            [-0.6128, 1.6326, 0.0187],
                                            [0.1407, -0.3380, -0.0044],
                                            [-0.1420, 0.2488, 0.0044],
                                            [0.1872, -0.3908, 0.9942],
                                            [-0.0451, 0.1420, 0.0013],
                                            [0.0222, -0.0253, -0.0004],
                                            [-0.0290, -0.0201, 0.0006],
                                            [0.0068, 0.0454, 0.9990]
                                          ],
                              DEUTERANOMALY: [[0.5442, -1.1454, 0.9818],
                                              [-0.7091, 1.5287, 0.0238],
                                              [0.1650, -0.3833, -0.0055],
                                              [-0.1664, 0.4368, 0.0056],
                                              [0.2178, -0.5327, 0.9927],
                                              [-0.0514, 0.0958, 0.0017],
                                              [0.0180, -0.0288, -0.0006],
                                              [-0.0232, -0.0649, 0.0007],
                                              [0.0052, 0.0360, 0.9998]
                                            ],
                              TRITANOMALY: [[0.4275, -0.0181, 0.9307],
                                            [-0.2454, 0.0013, 0.0827],
                                            [-0.1821, 0.0168, -0.0134],
                                            [-0.1280, 0.0047, 0.0202],
                                            [0.0233, -0.0398, 0.9728],
                                            [0.1048, 0.0352, 0.0070],
                                            [-0.0156, 0.0061, 0.0071],
                                            [0.3841, 0.2947, 0.0151],
                                            [-0.3685, -0.3008, 0.9778]]
  };

  var CVDAdjusmentParams = {PROTANOMALY: 
                            {RGBSpecific:[[0.0, 0.0, 0.0],
                                          [0.7, 1.0, 0.0],
                                          [0.7, 0.0, 1.0]],
                            deltaSpecific:[[0.0, 0.0, 0.0],
                                          [0.3, 0.0, 0.0],
                                          [-0.3, 0.0, 0.0]
                                        ]
                                      },
                          DEUTERANOMALY: {
                            RGBSpecific: [[0.0, 0.0, 0.0],
                                          [0.7, 1.0, 0.0],
                                          [0.7, 0.0, 1.0]],
                            deltaSpecific: [[0.0, 0.0, 0.0],
                                            [0.3, 0.0, 0.0],
                                            [-0.3, 0.0, 0.0]
                                          ]
                                        },
                          TRITANOMALY: {
                            RGBSpecific: [[1.0, 0.0, 0.7],
                                          [0.0, 1.0, 0.7],
                                          [0.0, 0.0, 0.0]],
                            deltaSpecific: [[0.0, 0.0, 0.3],
                                            [0.0, 0.0, -0.3],
                                            [0.0, 0.0, 0.0]]}
  };

  /**
  @param {string} cvdType 
  @param {number} severity
   */
  function CVDImitationMatrix(cvdType, severity) {
    var cvdSimulationParam = cvdSimulationParams[cvdType];
    var severity2 = severity * severity;
    var matrix = [];
    for (var i = 0; i < 3; i++) {
      var row = [];
      for (var j = 0; j < 3; j++) {
        var paramRow = i*3+j;
        var val = cvdSimulationParam[paramRow][0]*severity2 + cvdSimulationParam[paramRow][1]*severity + cvdSimulationParam[paramRow][2];
        row.push(val);
      }
      matrix.push(row);
    }
    return matrix;
  }

  /**
  @param {string} cvdType 
  @param {number} delta
   */
  function CVDAdjustmentMatrix(cvdType, delta) {
    CVDAdjustmentParam = CVDAdjusmentParams[cvdType];
    return matrixAddition(CVDAdjustmentParam['RGBSpecific'], matrixScalarMultiplication(CVDAdjustmentParam['deltaSpecific'], delta));
  }

  /**
  @param {string} cvdType
  @param {number} severity 
  @param {number} delta 
  @param {boolean} simulate 
  @param {boolean} enable 
   */
  function CVDEffectiveMatrix(cvdType, severity, delta, simulate, enable) {
    if (!enable) {
      return IdentityMatrix;
    }

    var effectiveMatrix = CVDImitationMatrix(cvdType, severity);

    if (!simulate) {
      var CVDAdjustedMatrix = CVDAdjustmentMatrix(cvdType, delta);
      var tempProduct = matrixMultiplication(CVDAdjustedMatrix, effectiveMatrix);

      effectiveMatrix = matrixSubtraction(matrixAddition(IdentityMatrix, CVDAdjustedMatrix), tempProduct);
    }
    return effectiveMatrix;
  }

  const STYLE_ID = 'cvd_style';
  const WRAP_ID = 'cvd_extension_svg_filter';

  function AddMissingElements() {
    var style = document.getElementById(STYLE_ID);
    if (!style) {
      var baseUrl = window.location.href.replace(window.location.hash, '');
      style = document.createElement('style');
      style.id = STYLE_ID;
      style.setAttribute('type', 'text/css');
      style.innerHTML = cssContent;
      document.head.appendChild(style);
    }

    var wrap = document.getElementById(WRAP_ID);
    if (!wrap) {
      wrap = document.createElement('span');
      wrap.id = WRAP_ID;
      wrap.setAttribute('hidden', '');
      wrap.innerHTML = svgContent;
      document.body.appendChild(wrap);
    }
  }

  /**
  @param {!Object} matrix  
   */
  function setFilter(matrix) {
    AddMissingElements();
    var next = 1 - curFilter;

    debugPrint('update: matrix#' + next + '=' + NewMatrixString(matrix));

    var matrixElem = document.getElementById('cvd_matrix_' + next);
    matrixElem.setAttribute('values', SVGMatrixString(matrix));

    document.documentElement.setAttribute('cvd', next);

    curFilter = next;
  }

  function update() {
    if (curEnable) {
      if (!document.body) {
        document.addEventListener('DOMContentLoaded', update);
        return;
      }
      var effectiveMatrix = CVDEffectiveMatrix(curType, curSeverity, curDelta*2-1, curSimulate, curEnable);
      setFilter(effectiveMatrix);
      if (window == window.top) {
        window.scrollBy(0, 1);
        window.scrollBy(0, -1);
      }
    } else {
      clearFilter();
    }
  }

  /**
  @param {!object} request
   */
  function onExtensionMessage(request) {
    debugPrint('onExtensionMessage: ' + JSON.stringify(request));
    var changed = false;

    if (request['type'] !== undefined) {
      var type = request.type;
      if (curType != type) {
        curType = type;
        changed = true;
      }
    }
    if (request['severity'] !== undefined) {
      var severity = request.severity;
      if (curSeverity != severity) {
        curSeverity = severity;
        changed = true;
      }
    }
    if (request['delta'] !== undefined) {
      var delta = request.delta;
      if (curDelta != delta) {
        curDelta = delta;
        changed = true;
      }
    }
    if (request['simulate'] !== undefined) {
      var simulate = request.simulate;
      if (curSimulate != simulate) {
        curSimulate = simulate;
        changed = true;
      }
    }
    if (request['enable'] !== undefined) {
      var enable = request.enable;
      if (curEnable != enable) {
        curEnable = enable;
        changed = true;
      }
    }

    if (changed) {
      update();
    }
  }

  function clearFilter() {
    document.documentElement.removeAttribute('cvd');
  }

  exports.initializeExtension = function () {
    chrome.extension.onRequest.addListener(onExtensionMessage);
    chrome.extension.sendRequest({'init': true}, onExtensionMessage);
  };

  /**
  @param {string} type 
  @param {number} severity 
   */
  exports.getDefaultCvdCorrectionFilter = function(type, severity) {
      return CVDEffectiveMatrix(type, severity, 0, false, true);
  };

  /**
  @param {!Object} matrix 
   */
  exports.injectColorEnhancementFilter = function(matrix) {
    setFilter(matrix);
  };

  exports.clearColorEnhancementFilter = function() {
    clearFilter();
  };
})(this);

this.initializeExtension();
