import { createWebHistory, createRouter } from "vue-router";
import Home from '../views/Home.vue';
import AnnotationMainPage from "@/views/annotators/AnnotationMainPage";
import TextFileUploadPage from "@/views/annotators/textfile/TextFileUploadHomePage";
import TextFileAnnotatorPage from "@/views/annotators/textfile/TextFileAnnotatorPage";
import ImageAnnotation from "@/views/annotators/image/ImageAnnotation";
import DBDetailsHomePage from "@/views/annotators/database/DBDetailsHomePage";
import DBAnnotatorPage from "@/views/annotators/database/DBAnnotatorPage"
import DFUploadPage from "@/views/annotators/dataframe/DFUploadPage";
import DFAnnotatorPage from "@/views/annotators/dataframe/DFAnnotatorPage";
import OCRMainPage from "@/views/ocr/OCRMainPage";
import Tessaract from "@/views/ocr/Tesseract.vue";
import Calamari from "@/views/ocr/Calamari";
import NERPage from "@/views/ner/NERPage";
import ImageHome from "@/views/annotators/image/ImageHome";
import ControlPanePage from "@/views/controlpane/ControlPanePage";
import LogIn from "@/views/LogIn";
import SignUp from "@/views/SignUp";

export const routes = [
  {
    path: '/',
    name: 'Login',
    component: LogIn,
    meta: { auth: true, title: 'Mozhi Login' }
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp,
    meta: { auth: true, title: 'Mozhi Login' }
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: { auth: true, title: 'Mozhi Home' }
  },
  {
    path: '/annotator/',
    name: 'AnnotationMainPage',
    component: AnnotationMainPage,
    meta: { auth: true, title: 'Mozhi AnnotationMainPage' }
  },
  {
    path: '/annotator/textfile',
    name: 'TextFileUploadPage',
    component: TextFileUploadPage,
    meta: { auth: true, title: 'Mozhi TextFileUploadPage' }
  },
  {
    path: '/annotator/text',
    name: 'Annotation',
    component: TextFileAnnotatorPage,
    meta: { auth: true, title: 'Mozhi TextFileAnnotatorPage' }
  },
  {
    path: '/annotator/imagefile',
    name: 'ImageAnnotation',
    component: ImageAnnotation,
    meta: { auth: true, title: 'Mozhi ImageAnnotation' }
  },
  {
    path: '/annotator/imagehome',
    name: 'ImageHome',
    component: ImageHome,
    meta: { auth: true, title: 'Mozhi ImageHome' }
  },

  {
    path: '/annotator/db',
    name: 'DBAnnotatorPage',
    component: DBAnnotatorPage,
    meta: { auth: true, title: 'Mozhi DBAnnotatorPage' }
  },
  {
    path: '/annotator/dbdetails',
    name: 'DBDetailsHomePage',
    component: DBDetailsHomePage,
    meta: { auth: true, title: 'Mozhi DBDetailsHomePage' }
  },
  {
    path: '/annotator/dffile',
    name: 'DFUploadPage',
    component: DFUploadPage,
    meta: { auth: true, title: 'Mozhi DFUploadPage' }
  },
  {
    path: '/annotator/df',
    name: 'DFAnnotator',
    component: DFAnnotatorPage,
    meta: { auth: true, title: 'Mozhi DFAnnotatorPage' }
  },
  {
    path: '/annotator/df',
    name: 'DFAnnotator',
    component: DFAnnotatorPage,
    meta: { auth: true, title: 'Mozhi Buckets' }
  },
  {
    path: '/ocr',
    name: 'OCRMainPage',
    component: OCRMainPage,
    meta: { auth: true, title: 'Mozhi OCRMainPage' }
  },
  {
    path: '/ocr/tesseract',
    name: 'Tesseract',
    component: Tessaract,
    meta: { auth: true, title: 'Mozhi Tesseract' }
  },
  {
    path: '/ocr/calamari',
    name: 'Calamari',
    component: Calamari,
    meta: { auth: true, title: 'Mozhi Calamari' }
  },
  {
    path: '/ner',
    name: 'NER',
    component: NERPage,
    meta: { auth: true, title: 'Mozhi NERPage' }
  },
  {
    path: '/controlpane',
    name: 'ControlPane',
    component: ControlPanePage,
    meta: { auth: true, title: 'Control Pane' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;