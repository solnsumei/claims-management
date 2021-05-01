import os
import img2pdf
import docx2pdf
import aiofiles
from PIL import Image
from datetime import datetime
from fastapi import Depends, BackgroundTasks, File, UploadFile
from .baserouter import BaseRouter
from src.models import User, Claim, ClaimPydantic, ClaimWithRelations
from src.models.schema.claim import CreateSchema, UpdateSchema, InvoiceUpdateAction
from src.utils.security import get_current_user, check_admin
from src.utils.exceptions import ForbiddenException, UnProcessableException
from src.utils.helpers import deletable_statuses, updatable_statuses, upload_folder
from src.utils.enums import InvoiceStatus
from src.services.mail_service import mail_service, create_welcome_message


router = BaseRouter()
image_extensions = [".jpg", ".jpeg"]
docs_extensions = [".doc", ".docx"]


@router.get("/")
async def fetch_all_claims(auth: User = Depends(get_current_user)):
    if auth.is_admin or auth.role == "Admin":
        return await ClaimWithRelations.from_queryset(Claim.all())
    return await ClaimWithRelations.from_queryset(Claim.filter(user_id=auth.id))


@router.get("/{claim_id}", response_model=ClaimWithRelations)
async def get_claim(claim_id: str, auth: User = Depends(get_current_user)):
    if auth.is_admin:
        return await ClaimWithRelations.from_queryset_single(Claim.get(id=claim_id))
    return await ClaimWithRelations.from_queryset_single(Claim.get(user_id=auth.id, id=claim_id))


@router.post("/{claim_id}/upload-file", status_code=200, response_model=ClaimPydantic)
async def upload_claim_file(
        claim_id: str,
        # background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        auth: User = Depends(get_current_user)):

    claim = await Claim.get(user_id=auth.id, id=claim_id)
    if claim.status != InvoiceStatus.New:
        raise UnProcessableException("Claims cannot be updated")

    try:
        # Todo - Convert to background task to convert file to pdf if it comes in other formats
        file_url = f"{upload_folder}/{claim.claim_id}.pdf"

        _, file_extension = os.path.splitext(file.filename)

        async with aiofiles.open(file_url, "wb") as f:
            content = await file.read()
            if file_extension in image_extensions:
                await f.write(img2pdf.convert(content))
            elif file_extension in docs_extensions:
                await f.write(docx2pdf.convert(content))
            else:
                await f.write(content)
        claim.file_url = file_url
        claim.status = InvoiceStatus.Pending
        await claim.save()
    except Exception:
        raise UnProcessableException("File upload could not be completed")
    finally:
        file.file.close()

    # Todo - Add background task to send mail to respective admins
    # message = create_welcome_message(
    #     name=user.name,
    #     email=[user.email],
    #     password=password,
    # )

    # background_tasks.add_task(mail_service.send_message, message)
    return await ClaimPydantic.from_tortoise_orm(claim)


@router.post("/", status_code=201, response_model=ClaimPydantic)
async def add_claim(
        claim: CreateSchema,
        auth: User = Depends(get_current_user)):

    claim.user_id = auth.id
    if auth.department is not None:
        claim.department_id = auth.department_id

    claims_no = "CLM-101"

    found_claim = await Claim.filter().order_by('-created_at').first()
    if found_claim is not None:
        str_list = found_claim.claim_id.split('-')
        next_claim = int(str_list[1]) + 1
        claims_no = f"CLM-{next_claim}"

    claim.claim_id = claims_no
    new_claim = await Claim.create_one(claim)

    return await ClaimPydantic.from_tortoise_orm(new_claim)


@router.put("/{claim_id}", response_model=ClaimPydantic, dependencies=[Depends(check_admin)])
async def update_claim(claim_id: str, claim: UpdateSchema):

    found_claim = await Claim.get(id=claim_id)
    if found_claim.status not in updatable_statuses:
        raise UnProcessableException("Claim cannot be updated")

    if found_claim.status != InvoiceUpdateAction.Approved \
            and claim.status == InvoiceUpdateAction.Approved:
        claim.approval_date = datetime.now()
        # Todo - Create and move file to month folder
        # Todo - Add task to send mail to employee or contractor

    updated_item = await Claim.update_one(claim_id, claim)
    return await ClaimPydantic.from_queryset_single(updated_item)


@router.delete("/{claim_id}", dependencies=[Depends(check_admin)])
async def delete_claim(claim_id: str):
    claim = await Claim.find_one(id=claim_id)

    if claim.status not in deletable_statuses:
        raise ForbiddenException("Approved or paid invoices cannot be deleted.")

    # Todo - delete file associated with claim

    success_message = {"message": "Item deleted successfully"}
    return success_message
