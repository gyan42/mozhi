import { createWebHistory, createRouter } from "vue-router";
import Home from '../views/Home.vue';
import AnnotationMainPage from "@/views/annotator/AnnotationMainPage";
import TextFileUploadPage from "@/views/annotator/textfile/TextFileUploadHomePage";
import TextFileAnnotatorPage from "@/views/annotator/textfile/TextFileAnnotatorPage";
import ImageAnnotation from "@/views/annotator/image/ImageAnnotation";
import DBDetailsHomePage from "@/views/annotator/db/DBDetailsHomePage";
import DBAnnotatorPage from "@/views/annotator/db/DBAnnotatorPage"
import DFUploadPage from "@/views/annotator/df/DFUploadPage";
import DFAnnotatorPage from "@/views/annotator/df/DFAnnotatorPage";
import OCRMainPage from "@/views/ocr/OCRMainPage";
import Tessaract from "@/views/ocr/Tesseract.vue";
import Calamari from "@/views/ocr/Calamari";
import NERPage from "@/views/ner/NERPage";
import ImageHome from "@/views/annotator/image/ImageHome";

export const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { auth: true, title: 'VF Home' }
  },
  {
    path: '/annotator/',
    name: 'AnnotationMainPage',
    component: AnnotationMainPage,
    meta: { auth: true, title: 'VF AnnotationMainPage' }
  },
  {
    path: '/annotator/textfile',
    name: 'TextFileUploadPage',
    component: TextFileUploadPage,
    meta: { auth: true, title: 'VF TextFileUploadPage' }
  },
  {
    path: '/annotator/text',
    name: 'Annotation',
    component: TextFileAnnotatorPage,
    meta: { auth: true, title: 'VF TextFileAnnotatorPage' }
  },
  {
    path: '/annotator/imagefile',
    name: 'ImageAnnotation',
    component: ImageAnnotation,
    meta: { auth: true, title: 'VF ImageAnnotation' }
  },
  {
    path: '/annotator/imagehome',
    name: 'ImageHome',
    component: ImageHome,
    meta: { auth: true, title: 'VF ImageHome' }
  },

  {
    path: '/annotator/db',
    name: 'DBAnnotatorPage',
    component: DBAnnotatorPage,
    meta: { auth: true, title: 'VF DBAnnotatorPage' }
  },
  {
    path: '/annotator/dbdetails',
    name: 'DBDetailsHomePage',
    component: DBDetailsHomePage,
    meta: { auth: true, title: 'VF DBDetailsHomePage' }
  },
  {
    path: '/annotator/dffile',
    name: 'DFUploadPage',
    component: DFUploadPage,
    meta: { auth: true, title: 'VF DFUploadPage' }
  },
  {
    path: '/annotator/df',
    name: 'DFAnnotator',
    component: DFAnnotatorPage,
    meta: { auth: true, title: 'VF DFAnnotatorPage' }
  },
  {
    path: '/annotator/df',
    name: 'DFAnnotator',
    component: DFAnnotatorPage,
    meta: { auth: true, title: 'VF Buckets' }
  },
  {
    path: '/ocr',
    name: 'OCRMainPage',
    component: OCRMainPage,
    meta: { auth: true, title: 'VF OCRMainPage' }
  },
  {
    path: '/ocr/tesseract',
    name: 'Tesseract',
    component: Tessaract,
    meta: { auth: true, title: 'VF Tesseract' }
  },
  {
    path: '/ocr/calamari',
    name: 'Calamari',
    component: Calamari,
    meta: { auth: true, title: 'VF Calamari' }
  },
  {
    path: '/ner',
    name: 'NER',
    component: NERPage,
    meta: { auth: true, title: 'VF NERPage' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;