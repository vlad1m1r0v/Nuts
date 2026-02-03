import {defineConfig} from 'vite';
import path from 'path';

export default defineConfig({
    base: '/static/',
    root: path.resolve(__dirname),
    build: {
        outDir: path.resolve(__dirname, '../static_vite/'),
        manifest: true,
        rollupOptions: {
            input: {
                // vendor js
                jquery_js: path.resolve(__dirname, 'src/js/vendor/jquery.min.js'),
                jquery_ui_js: path.resolve(__dirname, 'src/js/vendor/jquery-ui-1.10.4.custom.min.js'),
                count_to_js: path.resolve(__dirname, 'src/js/vendor/jquery.countTo.js'),
                swiper_js: path.resolve(__dirname, 'src/js/vendor/swiper.min.js'),
                simple_lightbox_js: path.resolve(__dirname, 'src/js/vendor/simple-lightbox.min.js'),
                scrollax_js: path.resolve(__dirname, 'src/js/vendor/scrollax.min.js'),
                picturefill_js: path.resolve(__dirname, 'src/js/vendor/picturefill.min.js'),
                stickyfill_js: path.resolve(__dirname, 'src/js/vendor/stickyfill.min.js'),
                m_custom_scrollbar_js: path.resolve(__dirname, 'src/js/vendor/jquery.mCustomScrollbar.js'),
                basictable_js: path.resolve(__dirname, 'src/js/vendor/jquery.basictable.min.js'),
                tooltipser_js: path.resolve(__dirname, 'src/js/vendor/tooltipster.bundle.min.js'),
                toastr_js: path.resolve(__dirname, 'src/js/vendor/toastr.min.js'),
                // common js
                common_js: path.resolve(__dirname, 'src/js/common.js'),
                // styles
                styles_js: path.resolve(__dirname, 'src/js/styles.js'),
            },
        },
    },
    server: {
        origin: 'http://localhost:5173',
    }
});