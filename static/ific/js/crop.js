



$('#wrapper').delegate('#signature-input', 'change', function () {
    if (!$(this).val()) return
    let value = $(this).val().replace(/^.*[\\\/]/, '')
    let truncatedString = value
    if (value.length > 13) {
        let start_string = value.substring(0, 9)
        let end_string = value.substring(value.length - 4, value.length)
        truncatedString = `${start_string}..${end_string}`
    }

    $(this).className += ' -chosen'

    $(this).next().next()[0].innerText = truncatedString
    read_image(this);

});


function read_image(input) {
    if (input.files && input.files[0]) {

        let reader = new FileReader();

        reader.onload = function (e) {

            var img = new Image();
            
            img.onload = function () {
                // if (img.width < 200 || img.height < 200) {
                //     alert('Sorry, the image you uploaded doesn\'t appear to be large enough.');
                //     return false;
                // }
                console.log("image loaded")
                cropImage(img);
                img.src = event.target.result;
                
            }
            

            let _text = $(input).text()
            $(input).val()
            $(input).text(_text)
        };

        reader.readAsDataURL(input.files[0]);
    }
}





function cropImage(originalImage) {

    $(originalImage).attr('id', 'fullImage');
    $('#signature_image').html(originalImage);

    var newImage = new imageCrop('#fullImage', 200, 200);

    $('#crop').on('click', function () {
        var results = newImage.crop();
        $('#thumbnail').html(results.img);
    });

}




var imageCrop = function (imageTarget, requiredWidth, requiredHeight) {
    // Variables
    var $doc = $(document),
        $cropMarker,
        $originalImage,
        origSrc = new Image(),
        imageTarget = $(imageTarget).get(0),
        imageScale,
        imageRatio,
        cropRatio,
        adjustedRequiredWidth,
        adjustedRequiredHeight,
        eventState = {},
        allowResize = true,
        keyboardMove = false,
        imageLoaded = new $.Deferred();

    origSrc.crossOrigin = "Anonymous";

    function init() {
        origSrc.onload = function () {
            // Check to make sure the target image is large enough
            if (origSrc.width < requiredWidth || origSrc.height < requiredHeight) {
                console.log('Image Crop error: The required dimensions are larger than the target image.');
                return false;
            }

            // And neccessary html
            $(imageTarget).wrap('<div class="ic-container"></div>').before('\
        <div class="ic-overlay-n" id="icOverlayN"></div>\
        <div class="ic-overlay-e" id="icOverlayE"></div>\
        <div class="ic-overlay-s" id="icOverlayS"></div>\
        <div class="ic-overlay-w" id="icOverlayW"></div>\
        <div class="ic-crop-marker" id="icCropMarker">\
            <div class="ic-resize-handle-nw" id="icResizeHandleNW"></div>\
            <div class="ic-resize-handle-ne" id="icResizeHandleNE"></div>\
            <div class="ic-resize-handle-sw" id="icResizeHandleSW"></div>\
            <div class="ic-resize-handle-se" id="icResizeHandleSE"></div>\
            <div class="ic-move-handle" id="icMoveHandle"></div>\
        </div>\
    ');
            $cropMarker = $('#icCropMarker');
            $originalImage = $(imageTarget);
            imageScale = origSrc.width / $originalImage.width();
            imageRatio = origSrc.width / origSrc.height;
            cropRatio = requiredWidth / requiredHeight;
            adjustedRequiredWidth = requiredWidth / imageScale;
            adjustedRequiredHeight = requiredHeight / imageScale;

            centerCropMarker();
            repositionOverlay();

            $cropMarker.on('mousedown touchstart', startResize);
            $cropMarker.on('mousedown touchstart', '#icMoveHandle', startMoving);
            imageLoaded.resolve();
        };
        origSrc.src = imageTarget.src;
    };

    function startResize(e) {
        e.preventDefault();
        e.stopPropagation();
        saveEventState(e);
        $doc.on('mousemove touchmove', resizing);
        $doc.on('mouseup touchend', endResize);
    };

    function endResize(e) {
        e.preventDefault();
        $doc.off('mouseup touchend', endResize);
        $doc.off('mousemove touchmove', resizing);
    };

    function resizing(e) {
        var mouse = {},
            width,
            height,
            left,
            top,
            originalWidth = $cropMarker.outerWidth(),
            originalHeight = $cropMarker.outerHeight(),
            originalOffset = $cropMarker.position();
        mouse.x = (e.clientX || e.pageX || e.originalEvent.touches[0].clientX) + $(window).scrollLeft();
        mouse.y = (e.clientY || e.pageY || e.originalEvent.touches[0].clientY) + $(window).scrollTop();

        var SE = false,
            SW = false,
            NW = false,
            NE = false;

        if ($(eventState.evnt.target).is('#icResizeHandleSE')) {
            SE = true;
        } else if ($(eventState.evnt.target).is('#icResizeHandleSW')) {
            SW = true;
        } else if ($(eventState.evnt.target).is('#icResizeHandleNW')) {
            NW = true;
        } else if ($(eventState.evnt.target).is('#icResizeHandleNE')) {
            NE = true;
        }

        if (SE) {
            width = mouse.x - eventState.containerLeft - $originalImage.offset().left;
            height = width / requiredWidth * requiredHeight;
            left = eventState.containerLeft;
            top = eventState.containerTop;
        } else if (SW) {
            width = eventState.containerWidth - (mouse.x - eventState.containerLeft - $originalImage.offset().left);
            height = width / requiredWidth * requiredHeight;
            left = mouse.x - $originalImage.offset().left;
            top = eventState.containerTop;
        } else if (NW) {
            width = eventState.containerWidth - (mouse.x - eventState.containerLeft - $originalImage.offset().left);
            height = width / requiredWidth * requiredHeight;
            left = mouse.x - $originalImage.offset().left;
            top = originalOffset.top + originalHeight - height;
        } else if (NE) {
            width = mouse.x - eventState.containerLeft - $originalImage.offset().left;
            height = width / requiredWidth * requiredHeight;
            left = eventState.containerLeft;
            top = originalOffset.top + originalHeight - height;
        }

        if (
            top >= 0 &&
            left >= 0 &&
            Math.round(top + height) <= Math.round($originalImage.height()) &&
            Math.round(left + width) <= Math.round($originalImage.width())
        ) {
            allowResize = true;
        }

        if (allowResize) {
            // Over top boundary
            if (top < 0) {
                height = originalHeight + originalOffset.top;
                width = height / requiredHeight * requiredWidth;
                top = 0;
                if (NW) {
                    left = originalOffset.left - (width - originalWidth);
                }
                allowResize = false;
            }
            // Over left boundary
            else if (left < 0) {
                width = originalWidth + originalOffset.left;
                height = width / requiredWidth * requiredHeight;
                left = 0;
                if (SE) {
                    top = originalOffset.top - (height - originalHeight);
                }
                allowResize = false;
            }
            // Over bottom boundary
            else if (Math.round(top + height) > Math.round($originalImage.height())) {
                height = $originalImage.height() - top;
                width = height / requiredHeight * requiredWidth;
                if (SW) {
                    left = originalOffset.left - (width - originalWidth);
                }
                allowResize = false;
            }
            // Over right boundary
            else if (Math.round(left + width) > Math.round($originalImage.width())) {
                width = $originalImage.width() - left;
                height = width / requiredWidth * requiredHeight;
                if (NE) {
                    top = originalOffset.top - (height - originalHeight);
                }
                allowResize = false;
            }

            // Check for min width / height
            if (width > adjustedRequiredWidth && height > adjustedRequiredHeight) {
                $cropMarker.outerWidth(width).outerHeight(height);
                $cropMarker.css({
                    'left': left,
                    'top': top
                });
            } else {
                if (SW || NW) {
                    left = left - (adjustedRequiredWidth - width);
                }
                if (NW || NE) {
                    top = top - (adjustedRequiredHeight - height);
                }
                $cropMarker.outerWidth(adjustedRequiredWidth).outerHeight(adjustedRequiredHeight);
                $cropMarker.css({
                    'left': left,
                    'top': top
                });
            }
        }
        repositionOverlay();
    }

    function startMoving(e) {
        e.preventDefault();
        e.stopPropagation();
        saveEventState(e);
        $doc.on('mousemove touchmove', moving);
        $doc.on('mouseup touchend', endMoving);
    };

    function endMoving(e) {
        e.preventDefault();
        $doc.off('mouseup touchend', endMoving);
        $doc.off('mousemove touchmove', moving);
    };

    function moving(e) {
        var top,
            left,
            mouse = {},
            touches;
        e.preventDefault();
        e.stopPropagation();

        touches = e.originalEvent.touches;

        mouse.x = (e.clientX || e.pageX || touches[0].clientX) + $(window).scrollLeft();
        mouse.y = (e.clientY || e.pageY || touches[0].clientY) + $(window).scrollTop();

        top = mouse.y - (eventState.mouseY - eventState.containerTop);
        left = mouse.x - (eventState.mouseX - eventState.containerLeft);
        if (top < 0) {
            top = 0;
        }
        if (top + $cropMarker.outerHeight() > $originalImage.height()) {
            top = $originalImage.height() - $cropMarker[0].getBoundingClientRect().height;
        }
        if (left < 0) {
            left = 0;
        }
        if (left + $cropMarker.outerWidth() > $originalImage.width()) {
            left = $originalImage.width() - $cropMarker[0].getBoundingClientRect().width;
        }
        $cropMarker.css({
            'top': top,
            'left': left
        });
        repositionOverlay();
    };

    document.addEventListener('keydown', function (e) {
        var top,
            left,
            shiftAmount,
            top = $cropMarker.position().top,
            left = $cropMarker.position().left;
        if (e.shiftKey) {
            shiftAmount = 10;
        } else {
            shiftAmount = 1;
        }

        if (e.keyCode === 37) {
            left = left - shiftAmount;
        } else if (e.keyCode === 38) {
            top = top - shiftAmount;
        } else if (e.keyCode === 39) {
            left = left + shiftAmount;
        } else if (e.keyCode === 40) {
            top = top + shiftAmount;
        }

        if (top < 0) {
            top = 0;
        }
        if (top + $cropMarker.outerHeight() > $originalImage.height()) {
            top = $originalImage.height() - $cropMarker[0].getBoundingClientRect().width;
        }
        if (left < 0) {
            left = 0;
        }
        if (left + $cropMarker.outerWidth() > $originalImage.width()) {
            left = $originalImage.width() - $cropMarker[0].getBoundingClientRect().width;
        }

        if (keyboardMove) {
            $cropMarker.css({
                'top': top,
                'left': left
            });
            repositionOverlay();
        }
    });

    $doc.click(function (e) {
        if ($(e.target).closest('.ic-container').length) {
            keyboardMove = true;
        } else {
            keyboardMove = false;
        }
    })

    var saveEventState = function (e) {
        eventState.containerWidth = $cropMarker.outerWidth();
        eventState.containerHeight = $cropMarker.outerHeight();
        eventState.containerLeft = $cropMarker.position().left;
        eventState.containerTop = $cropMarker.position().top;
        eventState.mouseX = (e.clientX || e.pageX || e.originalEvent.touches[0].clientX) + $(window).scrollLeft();
        eventState.mouseY = (e.clientY || e.pageY || e.originalEvent.touches[0].clientY) + $(window).scrollTop();
        eventState.evnt = e;
    };

    var centerCropMarker = function () {
        if (cropRatio > imageRatio) {
            $cropMarker.outerWidth($originalImage.width());
            $cropMarker.outerHeight($cropMarker.outerWidth() / requiredWidth * requiredHeight);
            $cropMarker.css({
                top: ($originalImage.height() - $cropMarker.height()) / 2 + 'px',
                left: 0
            });
        } else {
            $cropMarker.outerHeight($originalImage.height());
            $cropMarker.outerWidth($cropMarker.outerHeight() / requiredHeight * requiredWidth);
            $cropMarker.css({
                left: ($originalImage.width() - $cropMarker.width()) / 2 + 'px',
                top: 0
            });
        }
    }

    function repositionOverlay() {
        var imgWidth = $originalImage[0].getBoundingClientRect().width,
            imgHeight = $originalImage[0].getBoundingClientRect().height,
            cropTop = $cropMarker.position().top,
            cropLeft = $cropMarker.position().left,
            cropWidth = $cropMarker[0].getBoundingClientRect().width,
            cropHeight = $cropMarker[0].getBoundingClientRect().height,
            cropBorder = parseFloat($cropMarker.css('border-top-width'));
        $('#icOverlayN').css({
            right: imgWidth - cropLeft - cropWidth,
            height: cropTop,
            left: cropLeft
        });
        $('#icOverlayE').css({
            left: cropLeft + cropWidth
        });
        $('#icOverlayS').css({
            right: imgWidth - cropLeft - cropWidth,
            top: cropTop + cropHeight,
            left: cropLeft
        });
        $('#icOverlayW').css({
            width: cropLeft
        });
    };

    // Crop to required size
    this.crop = function () {
        var cropCanvas,
            img = new Image(),
            scale = origSrc.width / $originalImage.width(),
            left = Math.round($cropMarker.position().left * scale),
            top = Math.round($cropMarker.position().top * scale),
            width = Math.round($cropMarker.outerWidth() * scale),
            height = Math.round($cropMarker.outerHeight() * scale);
        results;

        cropCanvas = document.createElement('canvas');
        cropCanvas.width = requiredWidth;
        cropCanvas.height = requiredHeight;
        cropCanvas.getContext('2d').drawImage(origSrc, left, top, width, height, 0, 0, requiredWidth, requiredHeight);

        img.src = cropCanvas.toDataURL();

        var results = {
            img: img,
            left: left,
            top: top,
            width: width,
            height: height,
            requiredWidth: requiredWidth,
            requiredHeight: requiredHeight
        };
        return results;
    }

    this.position = function (left, top, width, height) {
        $.when(imageLoaded).done(function () {
            var scale = origSrc.width / $originalImage.width();
            left = Math.round(left / scale),
                top = Math.round(top / scale),
                width = Math.round(width / scale),
                height = Math.round(height / scale);
            $cropMarker.outerWidth(width).outerHeight(height);
            $cropMarker.css({
                'left': left,
                'top': top
            });
            repositionOverlay();
        });
    }

    this.cropReset = function () {
        centerCropMarker();
        repositionOverlay();
    }

    // Viewport resize
    $(window).resize(function () {
        imageScale = origSrc.width / $originalImage.width();
        adjustedRequiredWidth = requiredWidth / imageScale;
        adjustedRequiredHeight = requiredHeight / imageScale;
        centerCropMarker();
        repositionOverlay();
    });

    init();
};