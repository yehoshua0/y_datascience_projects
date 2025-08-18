# %%writefile data_augmentation_script.py

import google.generativeai as genai
from datasets import Dataset
import pandas as pd
import random
from typing import List, Dict
import time
from tqdm.auto import tqdm
import json
from kaggle_secrets import UserSecretsClient

user_secrets = UserSecretsClient()
secret_value_0 = user_secrets.get_secret("GEMINI_API_KEY")

# Configure Gemini API (replace with your actual API key)
genai.configure(api_key=secret_value_0)
model = genai.GenerativeModel('gemini-2.5-pro')

class KenyanHealthcareSyntheticDataGenerator:
    def __init__(self, original_dataset):
        self.original_dataset = original_dataset
        self.kenyan_counties = [
            "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu", "Kakamega",
            "Kiambu", "Machakos", "Kajiado", "Nyeri", "Meru", "Garissa", "Kitale",
            "Malindi", "Muranga", "Nyandarua", "Laikipia"
        ]
        self.health_levels = [
            "sub county hospitals and nursing homes", "national referral hospitals",
            "Level 2 Dispensary", "Level 3 Health Centre", "Level 4 Sub-County Hospital",
            "Level 5 County Hospital", "Level 6 National Hospital"
        ]
        self.nursing_competencies = [
            "pediatric emergency burns", "child health", "general emergency",
            "critical care", "adult health", "maternal and child health",
            "sexual and reproductive health"
        ]
        self.clinical_panels = [
            "surgery", "paediatrics", "internal medicine", "obstetrics and gynaecology"
        ]
        self.years_experience = list(range(5, 25))  # Range of experience years from dataset

    def analyze_original_patterns(self):
        """Analyze patterns in the original dataset to guide synthetic generation"""
        sample_prompts = self.original_dataset["Prompt"][:10]
        
        analysis_prompt = f"""
        Analyze these authentic Kenyan healthcare clinical prompts from the dataset:

        SAMPLE PROMPTS:
        {chr(10).join([f"{i+1}. {prompt}" for i, prompt in enumerate(sample_prompts)])}

        Please identify:
        1. Common structural patterns in how cases are presented (e.g., nurse introduction, patient demographics, symptoms, questions)
        2. Typical patient demographics and clinical presentations
        3. Resource constraints mentioned (e.g., lack of nebulizers, financial issues)
        4. Decision-making factors emphasized (e.g., immediate management, investigations)
        5. Cultural and contextual elements specific to Kenya (e.g., TB prevalence, socioeconomic factors)
        6. Language patterns and medical terminology used (e.g., local guidelines, abbreviations)

        Format your analysis as a structured guide for generating similar authentic cases, ensuring alignment with the dataset structure:
        - Master_Index: Unique identifier
        - County: Kenyan county
        - Health level: Facility type
        - Years of Experience: Nurse experience
        - Prompt: Clinical scenario with questions
        - Nursing Competency: Medical domain
        - Clinical Panel: Specialty area
        - Clinician: Nurse response
        - DDX SNOMED: Diagnosis codes
        """
        
        try:
            response = model.generate_content(analysis_prompt)
            return response.text
        except Exception as e:
            print(f"Error analyzing patterns: {e}")
            return "Generate realistic Kenyan healthcare cases with authentic clinical details."

    def generate_synthetic_case(self, nursing_competency: str, clinical_panel: str, patterns_guide: str) -> Dict[str, str]:
        """Generate a single synthetic case using Gemini"""
        
        county = random.choice(self.kenyan_counties)
        health_level = random.choice(self.health_levels)
        years_experience = random.choice(self.years_experience)
        master_index = f"ID_{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))}"
        
        generation_prompt = f"""
        You are an expert in Kenyan healthcare systems. Generate an authentic clinical case vignette that matches the patterns and quality of real cases from Kenyan healthcare facilities, aligned with the dataset structure.

        CONTEXT ANALYSIS:
        {patterns_guide}

        CASE PARAMETERS:
        - Nursing Competency: {nursing_competency}
        - Clinical Panel: {clinical_panel}
        - County: {county}
        - Health Level: {health_level}
        - Years of Experience: {years_experience}

        GENERATION REQUIREMENTS:
        1. Create a realistic clinical scenario that a nurse with {years_experience} years of experience would encounter at a {health_level} in {county}.
        2. Include specific details about:
           - Nurse introduction (e.g., "I am a nurse with {years_experience} years of experience in general nursing working in a {health_level} in {county}")
           - Patient demographics (age, gender, relevant background)
           - Clinical presentation and symptoms
           - Vital signs (e.g., BP, pulse, respiration, SpO2, temperature)
           - Specific questions for clinical decision-making
           - Available resources and constraints (e.g., limited equipment, financial issues)
           - Cultural or socioeconomic factors relevant to Kenya
        3. The case should require clinical reasoning and include 2-3 specific questions.
        4. Match the complexity level appropriate for the facility type.
        5. Include realistic constraints (staffing, equipment, referral options).
        6. End with a list of possible diagnoses (DDX SNOMED codes).

        OUTPUT FORMAT:
        - Master_Index: {master_index}
        - Prompt: [clinical scenario with questions]
        - DDX SNOMED: [list of relevant SNOMED codes]

        Generate ONLY the clinical prompt and SNOMED codes, 150-300 words, detailed and realistic.
        """

        try:
            response = model.generate_content(generation_prompt)
            response_text = response.text.strip()
            # Parse response to extract Prompt and DDX SNOMED
            prompt = response_text.split("Prompt:")[1].split("DDX SNOMED:")[0].strip()
            ddx_sno = response_text.split("DDX SNOMED:")[1].strip()
            return {
                "Master_Index": master_index,
                "County": county,
                "Health level": health_level,
                "Years of Experience": str(years_experience),
                "Prompt": prompt,
                "Nursing Competency": nursing_competency,
                "Clinical Panel": clinical_panel,
                "DDX SNOMED": ddx_sno
            }
        except Exception as e:
            print(f"Error generating case: {e}")
            return None

    def generate_clinical_response(self, prompt: str, context: Dict) -> str:
        """Generate appropriate clinical response for the synthetic case"""
        
        response_prompt = f"""
        You are a nurse with {context['Years of Experience']} years of experience working at a {context['Health level']} in {context['County']}, Kenya, specializing in {context['Nursing Competency']}.

        CLINICAL CASE:
        {prompt}

        Provide the clinical response that an experienced Kenyan nurse would give in this situation. Consider:
        1. Clinical assessment and differential diagnosis
        2. Immediate interventions within your scope and facility capabilities
        3. When to refer and to where (e.g., higher-level facility in {context['County']})
        4. Patient/family education and counseling
        5. Documentation and follow-up plans
        6. Resource constraints and practical limitations (e.g., limited equipment, Kenyan guidelines)

        Your response should be:
        - Clinically sound and appropriate for the {context['Health level']}
        - Practical given available resources
        - Culturally sensitive and aligned with Kenyan healthcare practices
        - 100-200 words
        - Written in the style of an experienced Kenyan healthcare professional

        Response:
        """

        try:
            response = model.generate_content(response_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""

    def generate_synthetic_dataset(self, num_samples: int = 200) -> Dataset:
        """Generate complete synthetic dataset aligned with the original dataset structure"""
        
        print("🔍 Analyzing original dataset patterns...")
        patterns_guide = self.analyze_original_patterns()
        
        print(f"🏥 Generating {num_samples} synthetic cases...")
        
        synthetic_data = []
        # Distribute samples across nursing competencies
        competency_distribution = [random.choice(self.nursing_competencies) for _ in range(num_samples)]
        panel_distribution = [random.choice(self.clinical_panels) for _ in range(num_samples)]
        
        for i, (competency, panel) in enumerate(tqdm(zip(competency_distribution, panel_distribution), total=num_samples, desc="Generating cases")):
            case_data = self.generate_synthetic_case(competency, panel, patterns_guide)
            
            if case_data:
                # Generate clinical response
                clinical_response = self.generate_clinical_response(
                    case_data["Prompt"], 
                    case_data
                )
                
                synthetic_data.append({
                    "Master_Index": case_data["Master_Index"],
                    "County": case_data["County"],
                    "Health level": case_data["Health level"],
                    "Years of Experience": case_data["Years of Experience"],
                    "Prompt": case_data["Prompt"],
                    "Nursing Competency": case_data["Nursing Competency"],
                    "Clinical Panel": case_data["Clinical Panel"],
                    "Clinician": clinical_response,
                    "GPT4.0": "",  # Placeholder for consistency
                    "LLAMA": "",    # Placeholder for consistency
                    "GEMINI": "",   # Placeholder for consistency
                    "DDX SNOMED": case_data["DDX SNOMED"]
                })
                
                # Rate limiting
                time.sleep(1)
            
            # Save progress every 50 samples
            if (i + 1) % 50 == 0:
                df = pd.DataFrame(synthetic_data)
                df.to_csv(f"synthetic_progress_{i+1}.csv", index=False)
                print(f"💾 Saved progress: {i+1} samples")

        print(f"✅ Generated {len(synthetic_data)} synthetic cases")
        return Dataset.from_pandas(pd.DataFrame(synthetic_data))

    def quality_filter_synthetic_data(self, synthetic_dataset: Dataset) -> Dataset:
        """Filter synthetic data for quality using Gemini"""
        
        print("🔍 Quality filtering synthetic data...")
        high_quality_samples = []
        
        for i, sample in enumerate(tqdm(synthetic_dataset, desc="Quality filtering")):
            quality_prompt = f"""
            Evaluate this synthetic Kenyan healthcare case for authenticity and quality:

            PROMPT: {sample['Prompt']}
            RESPONSE: {sample['Clinician']}
            DDX SNOMED: {sample['DDX SNOMED']}

            Rate on a scale of 1-10 considering:
            1. Clinical accuracy and realism
            2. Appropriate complexity for the {sample['Health level']}
            3. Authentic Kenyan healthcare context (e.g., {sample['County']} setting)
            4. Realistic resource constraints
            5. Cultural sensitivity and alignment with Kenyan medical practices
            6. Relevance of DDX SNOMED codes to the clinical scenario

            Provide only a single number (1-10) as your rating.
            """
            
            try:
                response = model.generate_content(quality_prompt)
                rating = float(response.text.strip())
                
                if rating >= 7.0:  # Keep high-quality samples
                    high_quality_samples.append(sample)
                    
            except Exception as e:
                print(f"Error rating sample {i}: {e}")
                continue
            
            # Rate limiting
            if i % 10 == 0:
                time.sleep(2)

        print(f"📊 Kept {len(high_quality_samples)} high-quality samples out of {len(synthetic_dataset)}")
        return Dataset.from_pandas(pd.DataFrame(high_quality_samples))

def main():
    # Load your original dataset
    df = pd.read_csv("/kaggle/input/updated-kenya-clinical-reasoning-challenge-dataset/train.csv")  # Adjust path as needed
    train_dataset = Dataset.from_pandas(df)
    
    # Initialize generator
    generator = KenyanHealthcareSyntheticDataGenerator(train_dataset)
    
    # Generate synthetic data
    synthetic_dataset = generator.generate_synthetic_dataset(num_samples=300)
    
    # Quality filter
    filtered_synthetic = generator.quality_filter_synthetic_data(synthetic_dataset)
    
    # Combine with original data
    from datasets import concatenate_datasets
    augmented_dataset = concatenate_datasets([train_dataset, filtered_synthetic]).shuffle(seed=42)
    
    print(f"🎯 Final dataset size: {len(augmented_dataset)}")
    print(f"📈 Augmentation ratio: {len(filtered_synthetic)/len(train_dataset):.2f}")
    
    # Save final dataset
    augmented_dataset.to_csv("augmented_train.csv")
    
    return augmented_dataset

def generate_few_shot_synthetic_data(original_dataset, num_samples=100):
    """Generate synthetic data using few-shot examples"""
    
    # Select diverse examples from original dataset
    sample_indices = random.sample(range(len(original_dataset)), min(5, len(original_dataset)))
    examples = [original_dataset[i] for i in sample_indices]
    
    few_shot_prompt = f"""
    Generate authentic Kenyan healthcare clinical cases similar to these examples, maintaining the dataset structure:

    EXAMPLES:
    {chr(10).join([f"Example {i+1}:{chr(10)}Master_Index: {ex['Master_Index']}{chr(10)}Prompt: {ex['Prompt']}{chr(10)}Clinician: {ex['Clinician']}{chr(10)}Nursing Competency: {ex['Nursing Competency']}{chr(10)}Clinical Panel: {ex['Clinical Panel']}{chr(10)}DDX SNOMED: {ex['DDX SNOMED']}{chr(10)}" for i, ex in enumerate(examples)])}

    Generate {num_samples} new cases following the same format, style, and quality.
    Each case should be unique but maintain the authentic Kenyan healthcare context.
    Vary the counties, facility types, patient demographics, years of experience, and medical conditions.
    Ensure all fields (Master_Index, County, Health level, Years of Experience, Prompt, Nursing Competency, Clinical Panel, Clinician, DDX SNOMED) are included.

    Format each as:
    Case X:
    Master_Index: [unique ID]
    County: [county]
    Health level: [facility type]
    Years of Experience: [years]
    Prompt: [clinical scenario with questions]
    Nursing Competency: [competency]
    Clinical Panel: [panel]
    Clinician: [clinical response]
    DDX SNOMED: [SNOMED codes]
    """
    
    try:
        response = model.generate_content(few_shot_prompt)
        return response.text
    except Exception as e:
        print(f"Error in few-shot generation: {e}")
        return None

if __name__ == "__main__":
    augmented_dataset = main()