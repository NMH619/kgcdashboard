/**

 * Gemini AI에게 질문을 던지는 커스텀 함수

 * @param {string} prompt 질문 내용

 * @return Gemini의 답변

 * @customfunction

 */

function gemini(prompt) {

  // 1. 발급받은 API 키를 여기에 넣으세요

  const apiKey = "여기에_아까_복사한_API_키를_넣으세요";

  const url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + apiKey;

  const payload = {

    "contents": [{

      "parts": [{

        "text": prompt

      }]

    }]

  };

  const options = {

    "method": "post",

    "contentType": "application/json",

    "payload": JSON.stringify(payload)

  };

  try {

    const response = UrlFetchApp.fetch(url, options);

    const json = JSON.parse(response.getContentText());

    

    // 답변 텍스트만 추출

    const result = json.candidates[0].content.parts[0].text;

    return result.trim();

  } catch (e) {

    return "에러 발생: " + e.toString();

  }

}


