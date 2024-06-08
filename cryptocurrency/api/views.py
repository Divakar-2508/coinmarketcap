from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.tasks import fetch_cryptocurrency_data
from .models import Job
from .serializers import JobSerializer

@api_view(['GET'])
def GetJobData(_request):
    job = Job.objects.all()
    serializer = JobSerializer(job, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ScrappingStatus(_request):
    job = Job.objects.get(job_id=_request.query_params["job_id"])

@api_view(['POST'])
def StartScraping(request):
    job = Job.objects.create()
    job_id = job.job_id
    print(request.data["coins"])
    for coin in request.data["coins"]:
        print("Called Function")
        fetch_cryptocurrency_data.delay(coin, job_id)
        print("Function Called")
    return Response({"job_id": job.job_id})