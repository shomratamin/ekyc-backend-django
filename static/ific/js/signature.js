var tmr;

var sigimage = document.getElementById("sigImg");

function onSign()
{
   var ctx = document.getElementById('cnv').getContext('2d');         
   SetDisplayXSize( 500 );
   SetDisplayYSize( 100 );
   SetTabletState(0, tmr);
   SetJustifyMode(0);
   ClearTablet();
   SetKeyString("0000000000000000");
   SetEncryptionMode(0);
   if(tmr == null)
   {
      tmr = SetTabletState(1, ctx, 50);
   }
   else
   {
      SetTabletState(0, tmr);
      tmr = null;
      tmr = SetTabletState(1, ctx, 50);
   }
}

function onClear()
{
   ClearTablet();
}

function onDone()
{
   if(NumberOfTabletPoints() == 0)
   {
      alert("Please sign before continuing");
   }
   else
   {
      SetTabletState(0, tmr); //deactivate connection

      //NOW, EXTRACT THE SIGNATURE IN THE TOPAZ BIOMETRIC FORMAT -- SIGSTRING
      //OR AS A BASE64-ENCODED PNG IMAGE
      //OR BOTH

      //********************USE THIS SECTION IF YOU WISH TO APPLY AUTOKEY TO YOUR TOPAZ SIGNATURE
      //READ ABOUT AUTOKEY AND THE TOPAZ SIGNATURE FORMAT HERE: http://topazsystems.com/links/robustsignatures.pdf
      //AUTOKEY IS CRITICAL TO SAVING AN eSIGN-COMPLIANT SIGNATURE
      //AUTOKEY ONLY APPLIES TO THE TOPAZ-FORMAT SIGSTRING AND DOES NOT APPLY TO AN IMAGE OF THE SIGNATURE
      //AUTOKEY ALLOWS THE DEVELOPER TO CRYPTOGRAPHICALLY BIND THE TOPAZ SIGNATURE TO A SET OF DATA
      //THE PURPOSE OF THIS IS TO SHOW THAT THE SIGNATURE IS BEING APPLIED TO THE DATA YOU PASS IN USING AutoKeyAddData()
      //IN GENERAL TOPAZ RECOMMENDS REPLICATING A TRADITIONAL 'PAPER AND PEN' APPROACH
      //IN OTHER WORDS, IF YOU WERE TO PRINT OUT ON PAPER THE TERMS/INFORMATION THE SIGNER IS SUPPOSED TO READ AND AGREE WITH
      //THE DATA ON THIS PAPER IS WHAT SHOULD IN WHOLE BE PASSED INTO AUTOKEYADDATA() DIGITALLY
      //THE TOPAZ SIGSTRING IS THEN BOUND TO THIS DATA, AND CAN ONLY BE SUCCESSFULLY DECRYPTED LATER USING THIS DATA
      var CryptoData = "";
      CryptoData = "This represents sample data the signer reads and is agreeing to when signing.";
      CryptoData = CryptoData + "Concatenate all this data into a single variable.";
      AutoKeyAddData(CryptoData); //PASS THE DATA IN TO BE USED FOR AUTOKEY
      SetEncryptionMode(2);
      //*******END AUTOKEY SECTION

      //NOTE THAT THE AUTOKEY SECTION ABOVE IS NOT REQUIRED TO RETURN A TOPAZ SIGSTRING
      //BUT IT IS STRONGLY RECOMMENDED IF YOU REQUIRE eSIGN COMPLIANCE
      //RETURN THE TOPAZ-FORMAT SIGSTRING
      SetSigCompressionMode(1);
      //alert("KEYSTRING:" + GetKeyString());
      //document.FORM1.bioSigData.value=GetSigString();
     // document.FORM1.sigStringData.value += GetSigString();
      //THIS RETURNS THE SIGNATURE IN TOPAZ'S OWN FORMAT WITH BIOMETRIC INFORMATION

      //TO RETURN THIS SIGSTRING LATER TO A NEW WEB PAGE USING SIGWEB, REPEAT THE CODE FROM THIS FUNCTION ABOVE STARTING AFTER SetTabletState(0, tmr)
      //BUT AT THE END USE SetSigString() INSTEAD OF GetSigString()
      //NOTE THAT SetSigString() TAKES 2 ARGUMENTS
      //SetSigString(str SigString, context canvas)

      //TO RETURN A BASE64-ENCODED PNG IMAGE OF THE SIGNATURE
      SetImageXSize(500);
      SetImageYSize(100);
      SetImagePenWidth(5);
      GetSigImageB64(SigImageCallback); //PASS IN THE FUNCTION NAME SIGWEB WILL USE TO RETURN THE FINAL IMAGE
   }
}


function SigImageCallback( str )
{   
   removeSigPreview();
   //sigimage.src= "data:image/jpeg;charset=utf-8;base64,"+str;
   x = "data:image/jpeg;charset=utf-8;base64,"+str;
   addSigPlaceholder(x);
}

function removeSigPreview() {
    document.getElementById("cnv").remove();
    document.getElementById("sig-actions").remove();
  }

  function addSigPlaceholder(sig) {

    console.log('hr');
  
    var sigDiv = document.createElement("div");
    sigDiv.className = "sig-image";
    sigDiv.id = "sig-container-tanvir";
    document.getElementById("sig-image").appendChild(sigDiv);
    var img = document.createElement("img");
    img.id = "sigImg";
    img.height = "100";
    img.width = "500";
    img.src = sig;
    document.getElementById("sig-container-tanvir").appendChild(img);
    // down.innerHTML = "Image Element Added.";
  } 